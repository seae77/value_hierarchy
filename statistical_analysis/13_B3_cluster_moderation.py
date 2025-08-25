#!/usr/bin/env python3
"""
13_B3_cluster_moderation.py

B3: Does cluster membership moderate the echo?
- For each block, fit PhaseII ~ PhaseI × Cluster + pair FE; participant-clustered SEs.
- Report simple slopes by cluster (C0 and C1) + interaction p; BH-FDR across blocks.

Inputs:
- data/processed/panel_long.parquet
- data/processed/cluster_assignments.csv
Output:
- tables/b3_cluster_moderation.tex
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import t as tdist

from .sa_utils import bh_fdr, effect_size_r_from_t, write_latex

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("13_B3")


def fit_block(df: pd.DataFrame, block: str) -> dict:
    sub = df[df["block"] == block].copy()
    if sub.empty:
        raise RuntimeError(f"No rows for block {block}")
    # Build design: PhaseI + pair FE + Cluster + PhaseI:Cluster
    d_pair = pd.get_dummies(sub["pair"], prefix="pair", drop_first=True)
    d_cluster = pd.get_dummies(sub["cluster"].astype(int), prefix="C", drop_first=True)  # C1 vs C0
    X = pd.concat([pd.Series(sub["PhaseI"], name="PhaseI"), d_cluster], axis=1)
    # Interaction
    if "C_1" in d_cluster.columns:
        X["PhaseI:C1"] = X["PhaseI"] * d_cluster["C_1"]
    else:
        X["PhaseI:C1"] = 0.0
    X = pd.concat([X, d_pair], axis=1)
    X = sm.add_constant(X)
    y = sub["PhaseII"].astype(float)
    res = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": sub["ResponseId"]})

    # Simple slopes
    b0 = float(res.params["PhaseI"])
    se0 = float(res.bse["PhaseI"])
    t0 = float(res.tvalues["PhaseI"])
    r0 = effect_size_r_from_t(t0, float(res.df_resid))
    ci0 = list(map(float, res.conf_int().loc["PhaseI"]))

    # Cluster 1 slope = PhaseI + PhaseI:C1
    if "PhaseI:C1" in res.params.index:
        est = float(res.params["PhaseI"] + res.params["PhaseI:C1"])
        var = (
            res.cov_params().loc["PhaseI", "PhaseI"]
            + res.cov_params().loc["PhaseI:C1", "PhaseI:C1"]
            + 2 * res.cov_params().loc["PhaseI", "PhaseI:C1"]
        )
        se1 = float(np.sqrt(max(var, 0)))
        t1 = est / se1 if se1 > 0 else np.nan
        r1 = effect_size_r_from_t(float(t1), float(res.df_resid))
        ci1 = [est - 1.96 * se1, est + 1.96 * se1]
        pint = float(res.pvalues["PhaseI:C1"])
    else:
        est, se1, t1, r1, ci1, pint = np.nan, np.nan, np.nan, np.nan, [np.nan, np.nan], np.nan

    return {
        "Block": block,
        "β C0": b0,
        "CI C0 lo": ci0[0],
        "CI C0 hi": ci0[1],
        "r C0": r0,
        "β C1": est,
        "CI C1 lo": ci1[0],
        "CI C1 hi": ci1[1],
        "r C1": r1,
        "p (interaction)": pint,
    }


def main(panel_parquet: Path, assign_csv: Path, out_latex: Path) -> None:
    df = pd.read_parquet(panel_parquet)
    assign = pd.read_csv(assign_csv).rename(columns=str)
    # Merge cluster labels (restricted to participants with labels)
    df = df.merge(assign[["ResponseId", "cluster"]], on="ResponseId", how="inner")

    rows = []
    for b in ["QH1", "QH2", "QH3", "QH5", "QH6"]:
        rows.append(fit_block(df, b))
    tab = pd.DataFrame(rows)
    tab["BH q"], _ = bh_fdr(tab["p (interaction)"].values, m=5)
    write_latex(
        tab,
        out_latex,
        caption="B3: Echo slopes by cluster (C0 vs C1) per block; BH-FDR over five interactions.",
        label="tab:cluster_moderation",
        float_format="{:.4f}",
    )
    logging.info(f"Wrote cluster moderation table: {out_latex}")


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="B3: cluster × echo moderation per block.")
    ap.add_argument("--panel", type=Path, default=Path("data/processed/panel_long.parquet"))
    ap.add_argument("--assign", type=Path, default=Path("data/processed/cluster_assignments.csv"))
    ap.add_argument("--out", type=Path, default=Path("tables/b3_cluster_moderation.tex"))
    args = ap.parse_args()
    main(args.panel, args.assign, args.out)
