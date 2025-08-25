#!/usr/bin/env python3
"""
07_A3_lobo_lopo.py

A-Branch A3: Robustness
- LOBO: leave-one-block-out
- LOPO: leave-one-pair-out
Model: overall OLS with pair FE + block FE; clustered by participant

Input: data/processed/panel_long.parquet
Output: two LaTeX tables
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

import pandas as pd

from .sa_utils import lobo, lopo, write_latex

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("07_A3")


def main(panel_parquet: Path, out_lobo: Path, out_lopo: Path) -> None:
    df = pd.read_parquet(panel_parquet)
    # LOBO
    lobo_df = lobo(df, block_col="block").rename(columns={"Left–out block": "Omitted block"})
    write_latex(
        lobo_df,
        out_lobo,
        caption="A3 LOBO: slope after omitting one block (overall model).",
        label="tab:a3_lobo",
        float_format="{:.4f}",
    )
    log.info(f"Wrote LOBO table: {out_lobo}")
    # LOPO
    lopo_df = lopo(df, pair_col="pair").rename(columns={"Left–out pair": "Omitted pair"})
    write_latex(
        lopo_df,
        out_lopo,
        caption="A3 LOPO: slope after omitting one pair (overall model).",
        label="tab:a3_lopo",
        float_format="{:.4f}",
    )
    log.info(f"Wrote LOPO table: {out_lopo}")


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="A3 LOBO/LOPO robustness")
    ap.add_argument("--panel", type=Path, default=Path("data/processed/panel_long.parquet"))
    ap.add_argument("--out-lobo", type=Path, default=Path("tables/a3_lobo.tex"))
    ap.add_argument("--out-lopo", type=Path, default=Path("tables/a3_lopo.tex"))
    args = ap.parse_args()
    main(args.panel, args.out_lobo, args.out_lopo)
