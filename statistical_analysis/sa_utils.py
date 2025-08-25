from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np
import pandas as pd
import statsmodels.api as sm
import yaml


# ---------- LaTeX utilities ----------
def write_latex(
    df: pd.DataFrame,
    out_path: Path,
    caption: str = "",
    label: str = "",
    float_format: str = "{:.3f}",
) -> None:
    """Write a DataFrame to a simple LaTeX table with caption and label.

    Numbers are formatted using the provided float_format string.
    """
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    # Build per-column formatters for numeric columns
    formatters = {}
    for c in df.columns:
        if pd.api.types.is_numeric_dtype(df[c]):
            formatters[c] = (
                lambda x, _fmt=float_format: ("" if pd.isna(x) else _fmt.format(float(x)))
            )

    table_content = df.to_latex(index=False, escape=False, formatters=formatters)
    content = (
        "\\begin{table}[htbp]\n"
        "\\centering\n"
        f"{table_content}\n"
        f"\\caption{{{caption}}}\n"
        f"\\label{{{label}}}\n"
        "\\end{table}\n"
    )
    out.write_text(content, encoding="utf-8")


# ---------- Stats helpers ----------
def bh_fdr(pvals: Sequence[float], m: int | None = None) -> Tuple[np.ndarray, np.ndarray]:
    """Benjamini–Hochberg FDR control.

    Returns (q_values, rejected_bool_array).
    If m is provided, use it as the total number of tests; else use len(pvals).
    """
    p = np.asarray(pvals, dtype=float)
    n = int(m) if m is not None else len(p)
    order = np.argsort(p)
    ranked = np.empty_like(order)
    ranked[order] = np.arange(1, len(p) + 1)
    q = (p * n) / ranked
    # Enforce monotonicity of q-values
    q_sorted = q[order]
    for i in range(len(q_sorted) - 2, -1, -1):
        q_sorted[i] = min(q_sorted[i], q_sorted[i + 1])
    q = np.empty_like(q_sorted)
    q[order] = q_sorted
    rejected = p <= (ranked / n) * 0.05
    return q, rejected


def effect_size_r_from_t(t_value: float, df: float) -> float:
    """Convert t-statistic to effect size r with sign of t."""
    if not np.isfinite(t_value) or not np.isfinite(df) or df <= 0:
        return float("nan")
    r = math.sqrt((t_value * t_value) / ((t_value * t_value) + df))
    return float(math.copysign(r, t_value))


def icc_2_1(r1: Sequence[float], r2: Sequence[float]) -> float:
    """Compute ICC(2,1) for two ratings (Shrout & Fleiss) with absolute agreement.

    Expects two arrays of equal length with potential NaNs. Returns NaN if insufficient data.
    """
    x = np.asarray(r1, dtype=float)
    y = np.asarray(r2, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    X = np.vstack([x[mask], y[mask]]).T  # shape (n, k=2)
    n, k = X.shape
    if n < 3:
        return float("nan")
    # Two-way random-effects ANOVA components
    mean_per_target = X.mean(axis=1)
    mean_per_rater = X.mean(axis=0)
    grand = X.mean()
    # Mean squares
    MSR = k * np.sum((mean_per_target - grand) ** 2) / (n - 1)
    MSC = n * np.sum((mean_per_rater - grand) ** 2) / (k - 1)
    MSE = (
        np.sum((X - mean_per_target[:, None] - mean_per_rater[None, :] + grand) ** 2)
        / ((k - 1) * (n - 1))
    )
    icc = (MSR - MSE) / (MSR + (k - 1) * MSE + (k * (MSC - MSE) / n))
    return float(icc)


# ---------- Models helpers ----------
def _add_pair_block_fe(df: pd.DataFrame, X: pd.DataFrame, pair_col: str | None, block_col: str | None) -> pd.DataFrame:
    mats = [X]
    if pair_col and pair_col in df.columns:
        mats.append(pd.get_dummies(df[pair_col], prefix="pair", drop_first=True))
    if block_col and block_col in df.columns:
        mats.append(pd.get_dummies(df[block_col], prefix="block", drop_first=True))
    return pd.concat(mats, axis=1)


def fit_ols_clustered(
    df: pd.DataFrame,
    y: str,
    x: str,
    group_col: str,
    add_const: bool = True,
    add_pair_fe: bool = False,
    pair_col: str | None = None,
    add_block_fe: bool = False,
    block_col: str | None = None,
):
    """Fit OLS y ~ x (+ FE) with participant-clustered SEs. Returns (result, design_matrix)."""
    work = df[[y, x, group_col] + ([pair_col] if (add_pair_fe and pair_col) else []) + ([block_col] if (add_block_fe and block_col) else [])].dropna().copy()
    X = pd.DataFrame({x: work[x].astype(float)})
    X = _add_pair_block_fe(work, X, pair_col if add_pair_fe else None, block_col if add_block_fe else None)
    if add_const:
        X = sm.add_constant(X)
    yv = work[y].astype(float)
    res = sm.OLS(yv, X).fit(cov_type="cluster", cov_kwds={"groups": work[group_col]})
    return res, X


def lobo(df: pd.DataFrame, block_col: str = "block") -> pd.DataFrame:
    """Leave-one-block-out slope for PhaseII ~ PhaseI (with pair and block FE)."""
    rows = []
    blocks = sorted(df[block_col].dropna().unique())
    for b in blocks:
        sub = df[df[block_col] != b]
        res, _ = fit_ols_clustered(
            sub,
            y="PhaseII",
            x="PhaseI",
            group_col="ResponseId",
            add_const=True,
            add_pair_fe=True,
            pair_col="pair",
            add_block_fe=True,
            block_col=block_col,
        )
        beta = float(res.params.get("PhaseI", np.nan))
        ci_lo, ci_hi = map(float, res.conf_int().loc["PhaseI"]) if "PhaseI" in res.params.index else (np.nan, np.nan)
        p = float(res.pvalues.get("PhaseI", np.nan))
        rows.append({"Omitted block": b, r"$\beta$": beta, "CI lo": ci_lo, "CI hi": ci_hi, r"$p$": p})
    return pd.DataFrame(rows)


def lopo(df: pd.DataFrame, pair_col: str = "pair") -> pd.DataFrame:
    """Leave-one-pair-out slope for PhaseII ~ PhaseI (with pair and block FE)."""
    rows = []
    pairs = sorted(df[pair_col].dropna().unique())
    for p in pairs:
        sub = df[df[pair_col] != p]
        res, _ = fit_ols_clustered(
            sub,
            y="PhaseII",
            x="PhaseI",
            group_col="ResponseId",
            add_const=True,
            add_pair_fe=True,
            pair_col=pair_col,
            add_block_fe=True,
            block_col="block",
        )
        beta = float(res.params.get("PhaseI", np.nan))
        ci_lo, ci_hi = map(float, res.conf_int().loc["PhaseI"]) if "PhaseI" in res.params.index else (np.nan, np.nan)
        pval = float(res.pvalues.get("PhaseI", np.nan))
        rows.append({"Omitted pair": p, r"$\beta$": beta, "CI lo": ci_lo, "CI hi": ci_hi, r"$p$": pval})
    return pd.DataFrame(rows)


# ---------- Config helpers ----------
@dataclass
class Pair:
    name: str


def load_pairs_config(pairs_yaml: Path) -> Tuple[List[Pair], Dict[str, str]]:
    """Load pairs from YAML. Accepts either a list of names or a mapping under 'pairs'."""
    data = yaml.safe_load(Path(pairs_yaml).read_text())
    names: List[str]
    if isinstance(data, dict) and "pairs" in data:
        if isinstance(data["pairs"], dict):
            names = list(data["pairs"].keys())
        else:
            names = [str(x) for x in data["pairs"]]
    elif isinstance(data, list):
        names = [str(x) for x in data]
    else:
        # Fallback: keys of dict
        names = list(data.keys())
    pairs = [Pair(name=n) for n in names]
    return pairs, {p.name: p.name for p in pairs}


def load_blocks_config(blocks_yaml: Path) -> Dict[str, Dict[str, str]]:
    """Load block→{pairName: columnName} mapping from YAML."""
    data = yaml.safe_load(Path(blocks_yaml).read_text())
    out: Dict[str, Dict[str, str]] = {}
    for block, spec in data.items():
        mapping = spec.get("mapping", {}) if isinstance(spec, dict) else {}
        out[block] = {str(k): str(v) for k, v in mapping.items()}
    return out


def extract_block_long(df_wide: pd.DataFrame, block: str, mapping: Dict[str, str]) -> pd.DataFrame:
    """Extract long form for a given block from wide df using mapping of pair→columnName."""
    rows = []
    for pair, col in mapping.items():
        if col in df_wide.columns:
            sub = pd.DataFrame({
                "ResponseId": df_wide["ResponseId"].astype(str),
                "pair": pair,
                "PhaseII": pd.to_numeric(df_wide[col], errors="coerce"),
                "block": block,
            })
            rows.append(sub)
    if not rows:
        return pd.DataFrame(columns=["ResponseId", "pair", "PhaseII", "block"])
    return pd.concat(rows, ignore_index=True)

