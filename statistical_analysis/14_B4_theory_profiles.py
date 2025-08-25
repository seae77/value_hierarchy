#!/usr/bin/env python3
"""
14_B4_theory_profiles.py

B4: Theory-driven moral profiles (Pro-Care, Pro-Tradition, Free-Spirit)
- Build signature scores per block per profile:
  * For each pair in a block: include only if exactly one value is focal (XOR)
  * If focal value appears second in the pair, invert PhaseII as (100 - raw)
  * Block signature = mean of oriented items
- Also build signature for Phase I (using Phase-I baseline per participant) via same orientation rule
- Report:
  * Profile-only model (averaged across blocks): means and contrasts (optional)
  * Block-wise adjusted means per profile
  * Echo within profile: PhaseII_signature ~ PhaseI_signature per block, OLS with clustered SEs

Inputs:
- data/processed/phase1_btpooled.csv
- data/interim/clean_phase1_phase2_raw.csv
- config/blocks.yaml (mapping of block→pair→column names)
Outputs:
- tables/b4_profiles_main.tex           (profile means across blocks)
- tables/b4_profile_block_means.tex     (profile × block adjusted means)
- tables/b4_profile_slopes.tex          (echo slopes per profile × block)
"""
from __future__ import annotations

import logging
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple

import numpy as np
import pandas as pd
import yaml
import statsmodels.api as sm

from .sa_utils import write_latex

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("14_B4")


VALUES = ["Care", "Fairness", "Loyalty", "Authority", "Sanctity", "Liberty"]
PROFILES: Dict[str, Set[str]] = {
    "ProCare": {"Care", "Fairness"},
    "ProTradition": {"Authority", "Loyalty"},
    "FreeSpirit": {"Sanctity", "Liberty"},
}


def load_block_maps(blocks_yaml: Path) -> Dict[str, Dict[str, str]]:
    data = yaml.safe_load(blocks_yaml.read_text())
    return {b: spec.get("mapping", {}) for b, spec in data.items()}


def split_pair_name(pair: str) -> Tuple[str, str]:
    # Split canonical name like "CareFairness" into ("Care","Fairness")
    for v in VALUES:
        if pair.startswith(v):
            R = pair[len(v) :]
            return v, R
    raise ValueError(f"Cannot split pair name: {pair}")


def signature_for_block(
    df_block: pd.DataFrame, mapping: Dict[str, str], focal: Set[str]
) -> pd.Series:
    """
    Compute block signature score for one profile:
    - df_block has columns for block items per participant (wide), plus ResponseId
    - mapping: {pairName: columnName}
    - For each pair: include XOR of focal membership; orient so higher=focal value
    """
    parts = []
    for pr, col in mapping.items():
        if col not in df_block.columns:
            continue
        L, R = split_pair_name(pr)
        xor = (L in focal) ^ (R in focal)
        if not xor:
            continue
        s = df_block[col].astype(float)
        # If focal is RIGHT (appears second in pair), invert 100 - raw
        if R in focal:
            s = 100.0 - s
        parts.append(s)
    if not parts:
        return pd.Series(np.nan, index=df_block.index)
    M = pd.concat(parts, axis=1)
    return M.mean(axis=1)  # average across oriented items


def signature_phase1(p1_df: pd.DataFrame, focal: Set[str]) -> pd.Series:
    """Compute Phase I signature per profile, using *_MEAN where available else *_REC, oriented as above."""
    parts = []
    for L in VALUES:
        for R in VALUES:
            if L == R:
                continue
            pr = f"{L}{R}"
            mean_col = f"P1Q-{pr}_MEAN"
            rec_col = f"P1Q-{pr}_REC"
            col = (
                mean_col
                if mean_col in p1_df.columns
                else rec_col if rec_col in p1_df.columns else None
            )
            if col is None:
                continue
            xor = (L in focal) ^ (R in focal)
            if not xor:
                continue
            s = p1_df[col].astype(float)
            if R in focal:
                s = 100.0 - s
            parts.append(s)
    if not parts:
        return pd.Series(np.nan, index=p1_df.index)
    M = pd.concat(parts, axis=1)
    return M.mean(axis=1)


def fit_echo_slope(
    y: pd.Series, x: pd.Series, ids: pd.Series
) -> Tuple[float, float, float, Tuple[float, float]]:
    """OLS y~x with participant-clustered SEs; return (beta, se, p, ci)."""
    df = pd.DataFrame({"y": y, "x": x, "id": ids}).dropna()
    if df.shape[0] < 10:
        return np.nan, np.nan, np.nan, (np.nan, np.nan)
    X = sm.add_constant(df["x"].astype(float).values)
    mod = sm.OLS(df["y"].astype(float).values, X)
    res = mod.fit(cov_type="cluster", cov_kwds={"groups": df["id"]})
    beta = float(res.params[1])
    se = float(res.bse[1])
    p = float(res.pvalues[1])
    ci = tuple(map(float, res.conf_int().iloc[1].values))
    return beta, se, p, ci


def main(
    clean_csv: Path,
    phase1_csv: Path,
    blocks_yaml: Path,
    out_profiles_main: Path,
    out_block_means: Path,
    out_profile_slopes: Path,
) -> None:
    df_wide = pd.read_csv(clean_csv)
    p1 = pd.read_csv(phase1_csv)
    maps = load_block_maps(blocks_yaml)

    # Block signatures per profile
    sig_block = defaultdict(list)  # keys: (profile, block)
    for prof, focal in PROFILES.items():
        for block, mapping in maps.items():
            s = signature_for_block(df_wide, mapping, focal)
            sig_block[(prof, block)].append(s.rename(f"{prof}_{block}"))

    # Build wide signatures DataFrame
    sig_wide = pd.DataFrame({"ResponseId": df_wide["ResponseId"].astype(str)})
    for (prof, block), series_list in sig_block.items():
        sig_wide[f"{prof}_{block}"] = series_list[0].values

    # Phase I signatures per profile
    for prof, focal in PROFILES.items():
        sig_wide[f"{prof}_P1"] = signature_phase1(p1, focal)

    # 1) Profile-only main (averaged across blocks)
    rows_main = []
    for prof in PROFILES:
        cols = [f"{prof}_{b}" for b in maps.keys() if f"{prof}_{b}" in sig_wide.columns]
        rows_main.append(
            {
                "Profile": prof,
                "Mean signature (across blocks)": float(sig_wide[cols].mean(axis=1).mean()),
            }
        )
    tab_main = pd.DataFrame(rows_main)
    write_latex(
        tab_main,
        out_profiles_main,
        caption="B4 Profile-only signature means (averaged across judgement contexts).",
        label="tab:profile_main",
        float_format="{:.2f}",
    )
    logging.info(f"Wrote B4 main profile table: {out_profiles_main}")

    # 2) Block-wise adjusted means per profile
    rows_adj = []
    for prof in PROFILES:
        for block in maps.keys():
            col = f"{prof}_{block}"
            if col in sig_wide.columns:
                rows_adj.append(
                    {"Profile": prof, "Block": block, "Mean signature": float(sig_wide[col].mean())}
                )
    tab_adj = pd.DataFrame(rows_adj)
    write_latex(
        tab_adj,
        out_block_means,
        caption="B4 Adjusted signature means by profile × judgement context.",
        label="tab:profile_block_means",
        float_format="{:.2f}",
    )
    logging.info(f"Wrote B4 block means table: {out_block_means}")

    # 3) Echo within profile: PhaseII_signature ~ PhaseI_signature (per block)
    rows_slopes = []
    for prof in PROFILES:
        for block in maps.keys():
            y = (
                sig_wide[f"{prof}_{block}"]
                if f"{prof}_{block}" in sig_wide.columns
                else pd.Series(dtype=float)
            )
            x = sig_wide[f"{prof}_P1"]
            beta, se, p, ci = fit_echo_slope(y, x, sig_wide["ResponseId"])
            rows_slopes.append(
                {
                    "Profile": prof,
                    "Block": block,
                    r"$\beta$": beta,
                    "SE": se,
                    "CI lo": ci[0],
                    "CI hi": ci[1],
                    r"$p$": p,
                }
            )
    tab_slopes = pd.DataFrame(rows_slopes)
    write_latex(
        tab_slopes,
        out_profile_slopes,
        caption="B4 Echo slopes within profiles by judgement context (signature scores).",
        label="tab:profile_slopes",
        float_format="{:.3f}",
    )
    logging.info(f"Wrote B4 profile slopes table: {out_profile_slopes}")


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(
        description="B4: theory-driven profiles — signature scores and echo."
    )
    ap.add_argument(
        "--clean-csv", type=Path, default=Path("data/interim/clean_phase1_phase2_raw.csv")
    )
    ap.add_argument("--phase1-csv", type=Path, default=Path("data/processed/phase1_btpooled.csv"))
    ap.add_argument("--blocks-yaml", type=Path, default=Path("config/blocks.yaml"))
    ap.add_argument("--out-profiles-main", type=Path, default=Path("tables/b4_profiles_main.tex"))
    ap.add_argument(
        "--out-block-means", type=Path, default=Path("tables/b4_profile_block_means.tex")
    )
    ap.add_argument("--out-profile-slopes", type=Path, default=Path("tables/b4_profile_slopes.tex"))
    args = ap.parse_args()
    main(
        args.clean_csv,
        args.phase1_csv,
        args.blocks_yaml,
        args.out_profiles_main,
        args.out_block_means,
        args.out_profile_slopes,
    )
