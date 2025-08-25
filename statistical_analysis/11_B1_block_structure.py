#!/usr/bin/env python3
"""
11_B1_block_structure.py

Block-level structure (B1): reliability & dimensionality
- For each Phase-II block, compute:
  * McDonald's ω_total (one-factor approximation using PCA loadings on z-scored items)
  * PCA variance explained by PC1 and PC2 (covariance on z-scored items)
- Input: cleaned wide participant-level CSV (after 01), blocks.yaml
- Output: LaTeX table with ω_total, %PC1, %PC2 per block

Notes:
- We approximate ω_total using unrotated PCA loadings on standardized variables:
    L = v1 * sqrt(ev1), communalities h_i^2 = L_i^2, uniqueness ψ_i = 1 - h_i^2
    omega_total = (sum(L_i))^2 / ((sum(L_i))^2 + sum(ψ_i))
- This is a standard approximation when a congeneric FA is not estimated.
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
import yaml
from sklearn.decomposition import PCA

from .sa_utils import write_latex

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("11_B1")


def load_block_maps(blocks_yaml: Path) -> Dict[str, Dict[str, str]]:
    data = yaml.safe_load(blocks_yaml.read_text())
    return {b: spec.get("mapping", {}) for b, spec in data.items()}


def zscore_cols(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    Z = df[cols].astype(float).copy()
    Z = (Z - Z.mean(axis=0)) / Z.std(axis=0, ddof=1)
    return Z


def omega_total_from_pca(Z: pd.DataFrame) -> float:
    """Approximate McDonald's ω_total using first principal component loadings on standardized variables."""
    X = Z.dropna(axis=0, how="any").values
    if X.shape[0] < 5:
        return float("nan")
    pca = PCA(n_components=2, random_state=2025)
    pca.fit(X)
    ev = pca.explained_variance_  # eigenvalues
    v1 = pca.components_[0, :]  # unit-length eigenvector
    L = v1 * np.sqrt(ev[0])  # loadings for PC1 on standardized vars
    h2 = L**2  # communalities
    psi = 1 - h2  # uniqueness on z-variables
    omega = (np.sum(L)) ** 2 / ((np.sum(L)) ** 2 + np.sum(psi))
    return float(omega)


def pca_var_explained(Z: pd.DataFrame) -> tuple[float, float]:
    X = Z.dropna(axis=0, how="any").values
    if X.shape[0] < 5:
        return float("nan"), float("nan")
    pca = PCA(n_components=2, random_state=2025)
    pca.fit(X)
    var_ratio = pca.explained_variance_ratio_ * 100.0
    pc1 = float(var_ratio[0])
    pc2 = float(var_ratio[1]) if len(var_ratio) > 1 else float("nan")
    return pc1, pc2


def main(clean_csv: Path, blocks_yaml: Path, out_latex: Path) -> None:
    df = pd.read_csv(clean_csv)
    block_maps = load_block_maps(blocks_yaml)

    rows = []
    for block, mapping in block_maps.items():
        cols = [c for c in mapping.values() if c in df.columns]
        if len(cols) < 3:
            log.warning(f"[{block}] only {len(cols)} columns found; skipping.")
            continue
        Z = zscore_cols(df, cols)
        omega = omega_total_from_pca(Z)
        pc1, pc2 = pca_var_explained(Z)
        rows.append(
            {
                "Block": block,
                "McDonald’s $\\omega_{\\text{total}}$": omega,
                "% variance PC1": pc1,
                "% variance PC2": pc2,
            }
        )

    tab = pd.DataFrame(rows).sort_values("Block")
    write_latex(
        tab,
        out_latex,
        caption="Block-level internal structure (McDonald's $\\omega_{\\text{total}}$; PCA %variance).",
        label="tab:block_structure",
        float_format="{:.3f}",
    )
    log.info(f"Wrote B1 structure table: {out_latex}")


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="B1: block-level reliability/dimensionality.")
    ap.add_argument(
        "--clean-csv", type=Path, default=Path("data/interim/clean_phase1_phase2_raw.csv")
    )
    ap.add_argument("--blocks-yaml", type=Path, default=Path("config/blocks.yaml"))
    ap.add_argument("--out", type=Path, default=Path("tables/b1_structure.tex"))
    args = ap.parse_args()
    main(args.clean_csv, args.blocks_yaml, args.out)
