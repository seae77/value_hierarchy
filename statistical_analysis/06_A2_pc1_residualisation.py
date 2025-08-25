#!/usr/bin/env python3
"""
06_A2_pc1_residualisation.py

A-Branch A2: Response-style correction (PC1)
- Residualise each of the 75 Phase-II items on [1, PC1]
- Rebuild a long panel of residualised PhaseII and original PhaseI
- Fit same A1 models per block
- Output LaTeX table with beta, CI, p, BH q (m=5), effect-size r

Inputs:
- data/interim/clean_phase1_phase2_raw.csv (participant-level wide)
- data/processed/phase1_btpooled.csv       (Phase-I predictors: *_MEAN/REC)
- data/interim/phase2_cols.json            (list of 75 Phase-II column names)
- config/pairs.yaml, config/blocks.yaml    (mapping pairs/blocks)

Assumes utils: io, pairs, models, stats, latex
"""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

from .sa_utils import (
    load_pairs_config,
    load_blocks_config,
    extract_block_long,
    fit_ols_clustered,
    bh_fdr,
    effect_size_r_from_t,
    write_latex,
)

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("06_A2")


def residualise_phase2_on_pc1(
    df_wide: pd.DataFrame, phase2_cols: list[str], pc1: pd.Series
) -> pd.DataFrame:
    """
    For each Phase-II column y, fit y ~ 1 + PC1 and replace with residuals.
    """
    X = np.column_stack([np.ones_like(pc1.values), pc1.values])
    df_res = df_wide.copy()
    for col in phase2_cols:
        y = df_wide[col].astype(float).values
        # handle NaNs: mask
        mask = ~np.isnan(y)
        if mask.sum() < 3:
            df_res[col] = np.nan
            continue
        # least squares on observed
        coef, *_ = np.linalg.lstsq(X[mask, :], y[mask], rcond=None)
        yhat = X @ coef
        resid = y - yhat
        df_res[col] = resid
    return df_res


def build_phase1_matrix(phase1_df: pd.DataFrame, pairs_yaml: Path) -> pd.DataFrame:
    pairs, _ = load_pairs_config(pairs_yaml)
    p1_map = {}
    for p in pairs:
        mean_col = f"P1Q-{p.name}_MEAN"
        rec_col = f"P1Q-{p.name}_REC"
        if mean_col in phase1_df.columns:
            p1_map[p.name] = mean_col
        elif rec_col in phase1_df.columns:
            p1_map[p.name] = rec_col
    p1_mat = pd.DataFrame({"ResponseId": phase1_df["ResponseId"].astype(str)})
    for nm, col in p1_map.items():
        p1_mat[nm] = phase1_df[col].astype(float)
    return p1_mat


def build_long_from_residuals(df_res: pd.DataFrame, blocks_yaml: Path) -> pd.DataFrame:
    block_maps = load_blocks_config(blocks_yaml)
    longs = []
    for block, mapping in block_maps.items():
        longs.append(extract_block_long(df_res, block, mapping))
    long_all = pd.concat(longs, ignore_index=True)
    return long_all


def fit_a2(long_res: pd.DataFrame, p1_mat: pd.DataFrame) -> pd.DataFrame:
    df = long_res.merge(
        p1_mat.melt(id_vars=["ResponseId"], var_name="pair", value_name="PhaseI"),
        on=["ResponseId", "pair"],
        how="left",
    ).dropna(subset=["PhaseI", "PhaseII"])
    rows = []
    for b in ["QH1", "QH2", "QH3", "QH5", "QH6"]:
        sub = df[df["block"] == b]
        res, covars = fit_ols_clustered(
            sub,
            y="PhaseII",
            x="PhaseI",
            group_col="ResponseId",
            add_const=True,
            add_pair_fe=True,
            pair_col="pair",
        )
        beta = float(res.params.get("PhaseI", np.nan))
        se = float(res.bse.get("PhaseI", np.nan))
        p = float(res.pvalues.get("PhaseI", np.nan))
        ci_lo, ci_hi = map(float, res.conf_int().loc["PhaseI"])
        r = effect_size_r_from_t(float(res.tvalues.get("PhaseI", np.nan)), float(res.df_resid))
        rows.append({"block": b, "beta": beta, "ci_lo": ci_lo, "ci_hi": ci_hi, "p": p, "r": r})
    tab = pd.DataFrame(rows)
    tab["q"], _ = bh_fdr(tab["p"].values, m=5)
    return tab


def main(
    clean_csv: Path,
    phase1_csv: Path,
    phase2_cols_json: Path,
    pc1_scores_csv: Path,
    pairs_yaml: Path,
    blocks_yaml: Path,
    out_latex: Path,
    caption: str,
    label: str,
) -> None:
    df_wide = pd.read_csv(clean_csv)
    p1_df = pd.read_csv(phase1_csv)
    phase2_cols = json.loads(Path(phase2_cols_json).read_text())
    pc1_df = pd.read_csv(pc1_scores_csv)
    pc1 = pd.Series(pc1_df["PC1"].values, index=pc1_df.index)

    # align indices (assumes the order of ResponseId matches; otherwise merge on id)
    df_wide = df_wide.merge(pc1_df[["ResponseId", "PC1"]], on="ResponseId", how="inner")
    pc1 = df_wide["PC1"]

    df_res = residualise_phase2_on_pc1(df_wide, phase2_cols, pc1)
    long_res = build_long_from_residuals(df_res, blocks_yaml)
    p1_mat = build_phase1_matrix(p1_df, pairs_yaml)

    tab = fit_a2(long_res, p1_mat)
    pretty = tab[["block", "beta", "ci_lo", "ci_hi", "p", "q", "r"]].copy()
    pretty.rename(
        columns={
            "block": "Block",
            "beta": r"$\beta$",
            "ci_lo": "CI lo",
            "ci_hi": "CI hi",
            "p": r"$p$",
            "q": "BH $q$",
            "r": r"$r$",
        },
        inplace=True,
    )
    write_latex(pretty, out_latex, caption=caption, label=label, float_format="{:.4f}")
    logging.info(f"Wrote LaTeX table: {out_latex}")


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="A2: echo after PC1 residualisation.")
    ap.add_argument(
        "--clean-csv", type=Path, default=Path("data/interim/clean_phase1_phase2_raw.csv")
    )
    ap.add_argument("--phase1-csv", type=Path, default=Path("data/processed/phase1_btpooled.csv"))
    ap.add_argument("--phase2-cols-json", type=Path, default=Path("data/interim/phase2_cols.json"))
    ap.add_argument("--pc1-scores-csv", type=Path, default=Path("data/processed/pc1_scores.csv"))
    ap.add_argument("--pairs-yaml", type=Path, default=Path("config/pairs.yaml"))
    ap.add_argument("--blocks-yaml", type=Path, default=Path("config/blocks.yaml"))
    ap.add_argument("--out", type=Path, default=Path("tables/a2_echo_postpc1.tex"))
    ap.add_argument(
        "--caption",
        default="A2 Echo slopes after residualising Phase-II on PC1; BH-FDR (m=5); effect-size $r$.",
    )
    ap.add_argument("--label", default="tab:a2_echo_postpc1")
    args = ap.parse_args()
    main(
        args.clean_csv,
        args.phase1_csv,
        args.phase2_cols_json,
        args.pc1_scores_csv,
        args.pairs_yaml,
        args.blocks_yaml,
        args.out,
        args.caption,
        args.label,
    )
