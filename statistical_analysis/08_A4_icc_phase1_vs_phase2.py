#!/usr/bin/env python3
"""
08_A4_icc_phase1_vs_phase2.py

A-Branch A4: ICC(2,1) between Phase-I baseline (BT-pooled) and mean Phase-II per pair.
- Input: cleaned wide Phase-II, Phase-I BT-pooled, blocks.yaml (to collect per-pair columns across blocks)
- Output: LaTeX table of ICC(2,1) per pair (optionally sorted)

Assumes:
- config/blocks.yaml maps each block {pairName: columnName}
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
import yaml

from .sa_utils import icc_2_1, write_latex

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("08_A4")


def load_block_maps(blocks_yaml: Path) -> Dict[str, Dict[str, str]]:
    data = yaml.safe_load(blocks_yaml.read_text())
    return {b: spec.get("mapping", {}) for b, spec in data.items()}


def main(
    clean_csv: Path, phase1_csv: Path, blocks_yaml: Path, out_latex: Path, caption: str, label: str
) -> None:
    df_wide = pd.read_csv(clean_csv)
    p1 = pd.read_csv(phase1_csv)
    block_maps = load_block_maps(blocks_yaml)

    # Build Phase-II mean per pair across five blocks
    pairs = sorted({pair for m in block_maps.values() for pair in m.keys()})
    means = pd.DataFrame({"ResponseId": df_wide["ResponseId"].astype(str)})
    for pr in pairs:
        cols = []
        for b, m in block_maps.items():
            col = m.get(pr, None)
            if col and col in df_wide.columns:
                cols.append(col)
        if len(cols) < 2:
            log.warning(f"Pair {pr}: only {len(cols)} block columns found.")
        means[pr] = df_wide[cols].astype(float).mean(axis=1)

    # Phase-I reference per pair (prefer MEAN else REC)
    p1_map = {}
    for pr in pairs:
        mean_col = f"P1Q-{pr}_MEAN"
        rec_col = f"P1Q-{pr}_REC"
        if mean_col in p1.columns:
            p1_map[pr] = p1[mean_col].astype(float)
        elif rec_col in p1.columns:
            p1_map[pr] = p1[rec_col].astype(float)
        else:
            p1_map[pr] = pd.Series(np.nan, index=p1.index)

    # Align participants (inner join on ResponseId)
    merged = means.merge(p1[["ResponseId"]], on="ResponseId", how="inner")
    # Compute ICC per pair
    rows = []
    for pr in pairs:
        r1 = p1_map[pr].values
        r2 = merged[pr].values
        # Align lengths: assume same order; if not, merge by ResponseId above
        icc = icc_2_1(r1, r2)
        rows.append({"pair": pr, "ICC(2,1)": icc})
    tab = pd.DataFrame(rows).sort_values("ICC(2,1)", ascending=False)
    write_latex(tab, out_latex, caption=caption, label=label, float_format="{:.3f}")
    log.info(f"Wrote ICC table: {out_latex}")


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="A4: ICC(2,1) Phase I vs mean Phase II per pair.")
    ap.add_argument(
        "--clean-csv", type=Path, default=Path("data/interim/clean_phase1_phase2_raw.csv")
    )
    ap.add_argument("--phase1-csv", type=Path, default=Path("data/processed/phase1_btpooled.csv"))
    ap.add_argument("--blocks-yaml", type=Path, default=Path("config/blocks.yaml"))
    ap.add_argument("--out", type=Path, default=Path("tables/a4_icc.tex"))
    ap.add_argument(
        "--caption", default="A4 ICC(2,1) between Phase I and mean Phase II scores per pair."
    )
    ap.add_argument("--label", default="tab:a4_icc")
    args = ap.parse_args()
    main(args.clean_csv, args.phase1_csv, args.blocks_yaml, args.out, args.caption, args.label)
