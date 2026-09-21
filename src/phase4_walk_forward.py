from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


CONFIG = json.loads(Path("config/phase4_walk_forward.json").read_text())
LEDGER = Path("data/derived/phase3_candidate_trade_ledger.csv")
OUT = Path("data/derived")
OUT.mkdir(parents=True, exist_ok=True)


def paired_bootstrap_ci(x: np.ndarray, reps: int, seed: int = 42) -> tuple[float, float]:
    if len(x) == 0:
        return np.nan, np.nan
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(x), size=(reps, len(x)))
    means = x[idx].mean(axis=1)
    return float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))


def paired_sign_flip_pvalue(x: np.ndarray, reps: int, seed: int = 43) -> float:
    if len(x) == 0:
        return np.nan
    rng = np.random.default_rng(seed)
    observed = abs(float(np.mean(x)))
    signs = rng.choice(np.array([-1.0, 1.0]), size=(reps, len(x)))
    simulated = np.abs((signs * x).mean(axis=1))
    return float((1 + np.sum(simulated >= observed)) / (reps + 1))


def candidate_ids(df: pd.DataFrame) -> list[str]:
    return sorted(df["candidate_id"].dropna().unique())


def metrics(g: pd.DataFrame) -> dict:
    valid = g[g["status"].fillna("").eq("")]
    gated = valid[valid["gate"].eq(True)]
    if len(valid) == 0:
        return {
            "valid_expiries": 0,
            "gated_trades": 0,
            "gate_rate": np.nan,
            "mean_pnl_per_expiry": np.nan,
            "mean_pnl_per_gated": np.nan,
            "win_rate": np.nan,
            "es95": np.nan,
            "es99": np.nan,
            "worst_pnl": np.nan,
        }
    pnl = valid["realized_net_pnl_inr"].fillna(0.0).to_numpy(float)
    losses = -gated["realized_net_pnl_inr"].to_numpy(float)
    return {
        "valid_expiries": int(len(valid)),
        "gated_trades": int(len(gated)),
        "gate_rate": float(len(gated) / len(valid)),
        "mean_pnl_per_expiry": float(np.mean(pnl)),
        "mean_pnl_per_gated": float(gated["realized_net_pnl_inr"].mean()) if len(gated) else np.nan,
        "win_rate": float(gated["win"].mean()) if len(gated) else np.nan,
        "es95": float(gated["es95_inr_proxy"].mean()) if len(gated) else np.nan,
        "es99": float(gated["es99_inr_proxy"].mean()) if len(gated) else np.nan,
        "worst_pnl": float(gated["realized_net_pnl_inr"].min()) if len(gated) else np.nan,
    }


def select_on_train(df: pd.DataFrame, baseline_id: str) -> pd.DataFrame:
    base_train = df[
        (df["candidate_id"] == baseline_id)
        & (df["window"] == "train")
    ]
    bm = metrics(base_train)
    rows = []
    for cid in candidate_ids(df):
        g = df[(df["candidate_id"] == cid) & (df["window"] == "train")]
        m = metrics(g)
        feasible = (
            m["gated_trades"] >= CONFIG["min_gated_trades"]
            and m["mean_pnl_per_expiry"] >= bm["mean_pnl_per_expiry"] * CONFIG["ev_retention"]
            and m["mean_pnl_per_gated"] >= bm["mean_pnl_per_gated"] * CONFIG["ev_retention"]
            and m["win_rate"] >= bm["win_rate"] - CONFIG["win_rate_tolerance"]
        )
        row = {
            "candidate_id": cid,
            **{f"train_{k}": v for k, v in m.items()},
            "feasible": bool(feasible),
        }
        rows.append(row)

    out = pd.DataFrame(rows)
    feasible = out[out["feasible"]].sort_values(
        ["train_es99", "train_es95", "train_gated_trades"],
        ascending=[True, True, False],
    )
    return out, feasible


def test_compare(df: pd.DataFrame, selected_id: str, baseline_id: str, window: str) -> dict:
    c = df[(df["candidate_id"] == selected_id) & (df["window"] == window)]
    b = df[(df["candidate_id"] == baseline_id) & (df["window"] == window)]
    cm = metrics(c)
    bm = metrics(b)

    c2 = c[["expiry", "gate", "realized_net_pnl_inr", "sensex_d3_gap_pct", "nifty_minus_sensex_prior20d_log_return"]].rename(
        columns={
            "gate": "candidate_gate",
            "realized_net_pnl_inr": "candidate_pnl",
        }
    )
    b2 = b[["expiry", "gate", "realized_net_pnl_inr", "sensex_d3_gap_pct", "nifty_minus_sensex_prior20d_log_return"]].rename(
        columns={
            "gate": "baseline_gate",
            "realized_net_pnl_inr": "baseline_pnl",
        }
    )
    m = b2.merge(c2, on="expiry", suffixes=("_b", "_c"))
    common = m[m["baseline_gate"].eq(True) & m["candidate_gate"].eq(True)].copy()
    deltas = (common["candidate_pnl"] - common["baseline_pnl"]).to_numpy(float) if len(common) else np.array([])

    lo, hi = paired_bootstrap_ci(deltas, CONFIG["bootstrap_reps"], seed=123)
    p = paired_sign_flip_pvalue(deltas, CONFIG["permutation_reps"], seed=456)

    test_threshold_gap = float(
        df[(df["window"] == "train")]["sensex_d3_gap_pct"].median()
    )
    test_threshold_rel = float(
        df[(df["window"] == "train")]["nifty_minus_sensex_prior20d_log_return"].median()
    )

    common["sensex_gap_regime"] = np.where(
        common["sensex_d3_gap_pct_b"] >= test_threshold_gap, "HIGH", "LOW"
    )
    common["relative_regime"] = np.where(
        common["nifty_minus_sensex_prior20d_log_return_b"] >= test_threshold_rel, "HIGH", "LOW"
    )

    regime_rows = []
    for col in ["sensex_gap_regime", "relative_regime"]:
        for regime in ["LOW", "HIGH"]:
            x = common[common[col] == regime]
            regime_rows.append({
                "window": window,
                "selected_candidate_id": selected_id,
                "baseline_id": baseline_id,
                "regime_field": col,
                "regime": regime,
                "n": int(len(x)),
                "mean_delta_pnl": float((x["candidate_pnl"] - x["baseline_pnl"]).mean()) if len(x) else np.nan,
                "candidate_mean_pnl": float(x["candidate_pnl"].mean()) if len(x) else np.nan,
                "baseline_mean_pnl": float(x["baseline_pnl"].mean()) if len(x) else np.nan,
            })

    return {
        "selected_candidate_id": selected_id,
        "baseline_candidate_id": baseline_id,
        "window": window,
        **{f"candidate_{k}": v for k, v in cm.items()},
        **{f"baseline_{k}": v for k, v in bm.items()},
        "common_gated_n": int(len(common)),
        "common_gate_mean_delta_pnl": float(np.mean(deltas)) if len(deltas) else np.nan,
        "paired_bootstrap_ci_low": lo,
        "paired_bootstrap_ci_high": hi,
        "paired_sign_flip_pvalue": p,
    }, regime_rows


def assign_windows(df: pd.DataFrame, split: dict) -> pd.DataFrame:
    d = df.copy()
    d["expiry_dt"] = pd.to_datetime(d["expiry"])
    train_end = pd.Timestamp(split["train_end"])
    test_start = pd.Timestamp(split["test_start"])
    d["window"] = np.where(
        d["expiry_dt"] <= train_end, "train",
        np.where(d["expiry_dt"] >= test_start, "test", "validation"),
    )
    return d


def main() -> None:
    df = pd.read_csv(LEDGER)
    df["status"] = df["status"].fillna("")
    baseline_id = "Q20p0_35p0_65p0_80p0"

    all_selection = []
    all_results = []
    all_regimes = []

    for split_name in ["split_a", "split_b"]:
        d = assign_windows(df, CONFIG[split_name])
        selection, feasible = select_on_train(d, baseline_id)

        # Always expose the control even when no candidate is feasible.
        selected_id = baseline_id
        if len(feasible):
            selected_id = str(feasible.iloc[0]["candidate_id"])

        selection["split"] = split_name
        selection["selected_candidate_id"] = selected_id
        all_selection.append(selection)

        if split_name == "split_a" and "validation" in d["window"].unique():
            result, regimes = test_compare(d, selected_id, baseline_id, "validation")
            result["split"] = split_name
            result["period_role"] = "validation"
            all_results.append(result)
            all_regimes.extend(regimes)

        result, regimes = test_compare(d, selected_id, baseline_id, "test")
        result["split"] = split_name
        result["period_role"] = "test"
        all_results.append(result)
        all_regimes.extend(regimes)

    pd.concat(all_selection, ignore_index=True).to_csv(
        OUT / "phase4_training_selection.csv", index=False
    )
    pd.DataFrame(all_results).to_csv(
        OUT / "phase4_walk_forward_results.csv", index=False
    )
    pd.DataFrame(all_regimes).to_csv(
        OUT / "phase4_sensex_regime_results.csv", index=False
    )

    summary = {
        "baseline_id": baseline_id,
        "split_count": 2,
        "bootstrap_reps": CONFIG["bootstrap_reps"],
        "permutation_reps": CONFIG["permutation_reps"],
        "sensex_regimes": [
            CONFIG["sensex_regime_field"],
            CONFIG["relative_regime_field"],
        ],
        "candidate_count": int(df["candidate_id"].nunique()),
    }
    (OUT / "phase4_run_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
