#!/usr/bin/env python3
"""
09_A5_context_interaction.py

A-Branch A5: Does echo differ by judgement context (block)?
- Fit a single model with PhaseI × Block (Choice ref), pair FE, clustered SEs.
- Report simple slopes per block (Choice + four contrasts)
- BH-FDR across five slopes; include effect-size r.

Input: data/processed/panel_long.parquet
Output: tables/a5_context_interaction.tex
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

from .sa_utils import bh_fdr, effect_size_r_from_t, write_latex

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("09_A5")


def fit_context_model(df: pd.DataFrame) -> tuple[sm.OLS, pd.DataFrame]:
    """
    PhaseII ~ PhaseI * block + pair FE ; cluster by participant.
    Choice (QH1) will be reference if we code dummies in alphabetical
    order and relevel the block accordingly.
    """
    work = df[["ResponseId", "PhaseII", "PhaseI", "pair", "block"]].dropna().copy()

    # Relevel block so QH1 is ref
    order = ["QH1", "QH2", "QH3", "QH5", "QH6"]
    work["block"] = pd.Categorical(work["block"], categories=order, ordered=True)

    # Pair FE
    fe_pair = pd.get_dummies(work["pair"], prefix="pair", drop_first=True)
    # Block dummies (drop first so QH1 is ref)
    fe_block = pd.get_dummies(work["block"], prefix="block", drop_first=True)
    X = pd.concat([pd.Series(work["PhaseI"], name="PhaseI"), fe_block], axis=1)

    # Add interactions PhaseI × block dummies
    for c in fe_block.columns:
        X[f"{c}:PhaseI"] = work["PhaseI"] * fe_block[c]

    # Add pair FE
    X = pd.concat([X, fe_pair], axis=1)
    X = sm.add_constant(X)
    y = work["PhaseII"].astype(float)
    mod = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": work["ResponseId"]})
    return mod, work


def simple_slope(mod: sm.OLS, term_phaseI: str, inter_terms: dict[str, str]) -> pd.DataFrame:
    """
    Compute simple slopes for each block:
    - For Choice (QH1): coefficient of 'PhaseI'
    - For others: PhaseI + interaction term
    """
    rows = []
    # Choice (reference)
    b = mod.params[term_phaseI]
    se = mod.bse[term_phaseI]
    p = mod.pvalues[term_phaseI]
    ci_lo, ci_hi = map(float, mod.conf_int().loc[term_phaseI])
    r = effect_size_r_from_t(float(mod.tvalues[term_phaseI]), float(mod.df_resid))
    rows.append(
        {"Block": "QH1", r"$\beta$": b, "CI lo": ci_lo, "CI hi": ci_hi, r"$p$": p, r"$r$": r}
    )

    # Others: linear combination
    for blk, inter in inter_terms.items():
        # slope = PhaseI + inter
        L = np.zeros_like(mod.params.values)
        L[list(mod.params.index).index(term_phaseI)] = 1.0
        L[list(mod.params.index).index(inter)] = 1.0
        est = float(L @ mod.params.values)
        # SE via variance of linear combination
        cov = mod.cov_params().values
        var = float(L @ cov @ L.T)
        se = np.sqrt(var)
        tval = est / se if se > 0 else np.nan
        from scipy.stats import t as tdist

        p = 2 * (1 - tdist.cdf(abs(tval), df=mod.df_resid))
        ci_lo, ci_hi = est - 1.96 * se, est + 1.96 * se
        r = effect_size_r_from_t(float(tval), float(mod.df_resid))
        rows.append(
            {"Block": blk, r"$\beta$": est, "CI lo": ci_lo, "CI hi": ci_hi, r"$p$": p, r"$r$": r}
        )
    return pd.DataFrame(rows)


def main(panel_parquet: Path, out_latex: Path) -> None:
    df = pd.read_parquet(panel_parquet)
    mod, work = fit_context_model(df)

    # Interaction terms mapping: block dummy names will be like 'block_QH2', etc.
    inter_terms = {
        "QH2": "block_QH2:PhaseI",
        "QH3": "block_QH3:PhaseI",
        "QH5": "block_QH5:PhaseI",
        "QH6": "block_QH6:PhaseI",
    }
    # Validate presence
    for v in inter_terms.values():
        if v not in mod.params.index:
            raise RuntimeError(f"Interaction term missing: {v}")

    tab = simple_slope(mod, term_phaseI="PhaseI", inter_terms=inter_terms)
    tab["BH $q$"], _ = bh_fdr(tab[r"$p$"].values, m=5)

    write_latex(
        tab,
        out_latex,
        caption="A5: Echo slopes by judgement context (Choice ref). BH-FDR (m=5); participant-clustered SEs; effect-size $r$.",
        label="tab:a5_context",
        float_format="{:.4f}",
    )
    logging.info(f"Wrote context-interaction table: {out_latex}")


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="A5: context moderation of echo (PhaseI × Block).")
    ap.add_argument("--panel", type=Path, default=Path("data/processed/panel_long.parquet"))
    ap.add_argument("--out", type=Path, default=Path("tables/a5_context_interaction.tex"))
    args = ap.parse_args()
    main(args.panel, args.out)
