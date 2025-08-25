#!/usr/bin/env python3
"""
01_load_clean_qualtrics.py
- Read Qualtrics (two header rows)
- Detect Phase I & Phase II slider columns (expect 9 + 75 = 84)
- Coerce numerics
- Apply participant-level filters:
    * Completeness >= 80% of 84 sliders
    * Flatliner (low variability) removal using combined SD+MAD over Phase-II items
- Save cleaned dataset and dropped log
- Save JSON lists of slider column names for downstream scripts
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd


def read_qualtrics_two_header(path: Path, sheet_name: str | None = None) -> pd.DataFrame:
    """Read a Qualtrics export with two header rows and flatten column names.

    - If Excel: uses the first two rows as a MultiIndex header and joins levels with " | ".
    - If CSV: reads normally with the first row as header.
    - Strips whitespace from column names.
    """
    path = Path(path)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        df = pd.read_excel(path, sheet_name=sheet_name, header=[0, 1])
        # Flatten multiindex columns
        flat_cols = []
        for col in df.columns:
            if isinstance(col, tuple):
                parts = [str(x) for x in col if str(x) != "nan"]
                flat_cols.append(" | ".join(parts).strip())
            else:
                flat_cols.append(str(col).strip())
        df.columns = flat_cols
    else:
        df = pd.read_csv(path)
        df.columns = [str(c).strip() for c in df.columns]
    return df


def to_csv(df: pd.DataFrame, out_path: Path, index: bool = False) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=index)


@dataclass
class CleaningConfig:
    slider_cols: List[str]
    phase2_cols: List[str]
    total_slider_expected: int = 84
    completeness_threshold: float = 0.80
    sd_floor: float = 4.0
    mad_floor: float = 3.0


def _coerce_numeric(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def apply_cleaning(df: pd.DataFrame, cfg: CleaningConfig) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Apply participant-level cleaning and return (kept, dropped).

    Steps:
    - Coerce slider columns to numeric
    - Completeness filter: require >= cfg.completeness_threshold of cfg.total_slider_expected
    - Flatliner filter: compute SD and MAD over Phase-II items; drop if SD < sd_floor and MAD < mad_floor
    """
    df = df.copy()
    df = _coerce_numeric(df, cfg.slider_cols)

    # Completeness across expected number of sliders
    present_cols = [c for c in cfg.slider_cols if c in df.columns]
    nonnull_counts = df[present_cols].notna().sum(axis=1)
    completeness = nonnull_counts / float(cfg.total_slider_expected)
    keep_mask = completeness >= cfg.completeness_threshold

    # Flatliner on Phase-II only
    p2_cols = [c for c in cfg.phase2_cols if c in df.columns]
    std_vals = df[p2_cols].astype(float).std(axis=1, ddof=0)
    mad_vals = (
        (df[p2_cols].astype(float) - df[p2_cols].astype(float).median(axis=1).values.reshape(-1, 1))
        .abs()
        .median(axis=1)
    )
    flat_mask = (std_vals < cfg.sd_floor) & (mad_vals < cfg.mad_floor)

    keep_final = keep_mask & (~flat_mask)

    kept = df.loc[keep_final].reset_index(drop=True)
    dropped = df.loc[~keep_final].copy()
    reasons = []
    for i in dropped.index:
        r = []
        if not keep_mask.iloc[i]:
            r.append("incomplete")
        if flat_mask.iloc[i]:
            r.append("flatliner")
        reasons.append(";".join(r) if r else "other")
    dropped["drop_reason"] = reasons
    dropped = dropped.reset_index(drop=True)
    return kept, dropped


logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("01_load_clean_qualtrics")


def detect_slider_columns(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    """
    Detect slider columns for Phase I and Phase II by prefix convention:
      - Phase I: columns starting with 'P1Q-'
      - Phase II: columns starting with 'QH1-', 'QH2-', 'QH3-', 'QH5-', 'QH6-'
    Returns (all_84, phase2_75) as lists in a stable sorted order.
    """
    p1 = sorted([c for c in df.columns if isinstance(c, str) and c.startswith("P1Q-")])
    phase2 = []
    for pref in ["QH1-", "QH2-", "QH3-", "QH5-", "QH6-"]:
        phase2.extend([c for c in df.columns if isinstance(c, str) and c.startswith(pref)])
    phase2 = sorted(phase2)
    all_ = sorted(p1 + phase2)
    return all_, phase2


def main(
    input_xlsx: Path,
    out_clean_csv: Path,
    out_drop_csv: Path,
    out_slider_json: Path,
    out_phase2_json: Path,
    sheet: str | None = None,
    completeness_threshold: float = 0.80,
    sd_floor: float = 4.0,
    mad_floor: float = 3.0,
) -> None:
    df = read_qualtrics_two_header(input_xlsx, sheet_name=sheet)

    # Basic admin filters: Finished == True, non-empty ResponseId
    if "Finished" in df.columns:
        df = df[df["Finished"].astype(str).str.lower().str.strip() == "true"].copy()
    if "ResponseId" not in df.columns:
        raise RuntimeError("ResponseId column required but not found after import.")
    df = df[~df["ResponseId"].astype(str).str.strip().eq("")].copy()
    df = df.drop_duplicates(subset=["ResponseId"], keep="first").reset_index(drop=True)

    # Detect slider columns
    all_sliders, phase2_sliders = detect_slider_columns(df)
    if len(all_sliders) < 70:
        log.warning(f"Unusually few slider columns detected: {len(all_sliders)}")

    # Save JSON lists (downstream scripts need them)
    out_slider_json.parent.mkdir(parents=True, exist_ok=True)
    out_slider_json.write_text(json.dumps(all_sliders, indent=2), encoding="utf-8")
    out_phase2_json.write_text(json.dumps(phase2_sliders, indent=2), encoding="utf-8")
    log.info(
        f"Saved slider lists:\n  all sliders -> {out_slider_json}\n  phase2     -> {out_phase2_json}"
    )

    # Apply cleaning
    cfg = CleaningConfig(
        slider_cols=all_sliders,
        phase2_cols=phase2_sliders,
        total_slider_expected=84,
        completeness_threshold=completeness_threshold,
        sd_floor=sd_floor,
        mad_floor=mad_floor,
    )
    kept, dropped = apply_cleaning(df, cfg)

    # Save outputs
    to_csv(kept, out_clean_csv)
    to_csv(dropped, out_drop_csv)
    log.info(f"Final kept N={len(kept)}; dropped N={len(dropped)}")


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Load & clean Qualtrics raw export (two header rows).")
    ap.add_argument("input_xlsx", type=Path)
    ap.add_argument("--sheet", default=None)
    ap.add_argument(
        "--out-clean-csv", type=Path, default=Path("data/interim/clean_phase1_phase2_raw.csv")
    )
    ap.add_argument("--out-drop-csv", type=Path, default=Path("data/interim/dropped_log.csv"))
    ap.add_argument(
        "--out-slider-json", type=Path, default=Path("data/interim/all_slider_cols.json")
    )
    ap.add_argument("--out-phase2-json", type=Path, default=Path("data/interim/phase2_cols.json"))
    ap.add_argument(
        "--threshold", type=float, default=0.80, help="completeness threshold over 84 sliders"
    )
    ap.add_argument("--sd-floor", type=float, default=4.0)
    ap.add_argument("--mad-floor", type=float, default=3.0)
    args = ap.parse_args()

    main(
        args.input_xlsx,
        args.out_clean_csv,
        args.out_drop_csv,
        args.out_slider_json,
        args.out_phase2_json,
        sheet=args.sheet,
        completeness_threshold=args.threshold,
        sd_floor=args.sd_floor,
        mad_floor=args.mad_floor,
    )
