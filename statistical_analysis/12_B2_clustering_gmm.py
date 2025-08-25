#!/usr/bin/env python3
"""
12_B2_clustering_gmm.py

B2: Participant clustering on six-slope vectors (overall + five blocks)
- For each participant, compute echo slopes:
  * Overall: PhaseII ~ PhaseI across all 75 items (pair FE + block FE cannot be fit per person; so we use simple OLS y~x)
  * Per block: PhaseII ~ PhaseI across that block's 15 pairs
- Assemble 6-D feature, z-score across participants
- Fit GMM for k=1..4; select k by BIC
- Report: chosen k, cluster sizes, silhouette mean; bootstrap Jaccard stability (approximate)

Inputs:
- data/processed/panel_long.parquet
Outputs:
- data/processed/cluster_assignments.csv (ResponseId, cluster)
- tables/b2_cluster_sizes_metrics.tex
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment
from sklearn.metrics import silhouette_score
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

from .sa_utils import write_latex

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("12_B2")


def slope_per_person(sub: pd.DataFrame) -> float:
    """Simple OLS slope PhaseII ~ PhaseI for one participant and subset (ignore FE; 15 points suffice)."""
    x = sub["PhaseI"].astype(float).values
    y = sub["PhaseII"].astype(float).values
    mask = ~np.isnan(x) & ~np.isnan(y)
    if mask.sum() < 3:
        return np.nan
    X = np.column_stack([np.ones(mask.sum()), x[mask]])
    coef, *_ = np.linalg.lstsq(X, y[mask], rcond=None)
    return float(coef[1])


def build_feature_matrix(df: pd.DataFrame) -> pd.DataFrame:
    feats = []
    for pid, g in df.groupby("ResponseId"):
        row = {"ResponseId": pid}
        # Overall slope (all blocks)
        row["Overall"] = slope_per_person(g)
        # Per block
        for b, gb in g.groupby("block"):
            row[b] = slope_per_person(gb)
        feats.append(row)
    X = pd.DataFrame(feats)
    # Ensure all expected blocks present
    for b in ["QH1", "QH2", "QH3", "QH5", "QH6"]:
        if b not in X.columns:
            X[b] = np.nan
    return X


def fit_gmm_bic(Xz: np.ndarray, k_min: int = 1, k_max: int = 4, seed: int = 1337) -> tuple[GaussianMixture, Dict[int, float]]:
    bics = {}
    best = None
    for k in range(k_min, k_max+1):
        gm = GaussianMixture(n_components=k, covariance_type="diag", random_state=seed)
        gm.fit(Xz)
        bics[k] = gm.bic(Xz)
        if best is None or bics[k] < bics[best.n_components]:
            best = gm
    return best, bics


def jaccard_stability(Xz: np.ndarray, base_labels: np.ndarray, k: int, n_boot: int = 200, subsample: float = 0.9, seed: int = 2025) -> np.ndarray:
    """
    Approximate bootstrap Jaccard stability:
    - Subsample participants (size ≈ 0.9N) without replacement
    - Fit GMM(k) to subsample
    - Compute cluster-wise Jaccard against base labels restricted to subsample
    Returns mean Jaccard per base cluster.
    """
    rng = np.random.default_rng(seed)
    N = Xz.shape[0]
    base = base_labels
    jaccs = []
    for _ in range(n_boot):
        idx = rng.choice(N, size=int(N*subsample), replace=False)
        gm = GaussianMixture(n_components=k, covariance_type="diag", random_state=int(rng.integers(0, 1e9)))
        gm.fit(Xz[idx])
        lab_b = base[idx]
        lab_s = gm.predict(Xz[idx])
        # match clusters by Hungarian on confusion counts
        K = k
        conf = np.zeros((K, K), dtype=int)
        for i in range(K):
            for j in range(K):
                conf[i, j] = np.sum((lab_b == i) & (lab_s == j))
        r, c = linear_sum_assignment(conf.max() - conf)
        # Jaccard for matched pairs
        j = []
        for i_b, j_s in zip(r, c):
            inter = conf[i_b, j_s]
            union = np.sum(lab_b == i_b) + np.sum(lab_s == j_s) - inter
            j.append(inter / union if union > 0 else 0.0)
        jaccs.append(j)
    return np.array(jaccs).mean(axis=0)


def main(panel_parquet: Path, out_assign: Path, out_latex: Path) -> None:
    df = pd.read_parquet(panel_parquet)
    X = build_feature_matrix(df)
    # Keep only rows with non-NaN across the 6 dims
    feat_cols = ["Overall", "QH1", "QH2", "QH3", "QH5", "QH6"]
    X2 = X.dropna(subset=feat_cols).reset_index(drop=True)
    scaler = StandardScaler()
    Xz = scaler.fit_transform(X2[feat_cols].values)

    gm, bics = fit_gmm_bic(Xz, 1, 4, seed=1337)
    labels = gm.predict(Xz)
    sil = silhouette_score(Xz, labels) if gm.n_components > 1 else np.nan
    jacc = jaccard_stability(Xz, labels, k=gm.n_components, n_boot=200)

    # Save assignments
    out_assign.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"ResponseId": X2["ResponseId"].astype(str), "cluster": labels}).to_csv(out_assign, index=False)

    # Table
    sizes = pd.Series(labels).value_counts().sort_index()
    rows = [{
        "k": gm.n_components,
        "BIC(k=1)": bics.get(1, np.nan),
        "BIC(k=2)": bics.get(2, np.nan),
        "BIC(k=3)": bics.get(3, np.nan),
        "BIC(k=4)": bics.get(4, np.nan),
        "Silhouette": sil,
        "Cluster 0 size": sizes.get(0, 0),
        "Cluster 1 size": sizes.get(1, 0),
        "Jaccard C0": jacc[0] if len(jacc) > 0 else np.nan,
        "Jaccard C1": jacc[1] if len(jacc) > 1 else np.nan,
    }]
    tab = pd.DataFrame(rows)
    write_latex(tab, out_latex,
                caption="B2 GMM clustering on six-slope vectors: BIC, silhouette, stability (bootstrap Jaccard).",
                label="tab:b2_cluster_sizes_metrics", float_format="{:.3f}")
    logging.info(f"Wrote B2 clustering table: {out_latex}")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="B2: GMM clustering of six-slope features (overall + five blocks).")
    ap.add_argument("--panel", type=Path, default=Path("data/processed/panel_long.parquet"))
    ap.add_argument("--out-assign", type=Path, default=Path("data/processed/cluster_assignments.csv"))
    ap.add_argument("--out", type=Path, default=Path("tables/b2_cluster_sizes_metrics.tex"))
    args = ap.parse_args()
    main(args.panel, args.out_assign, args.out)
