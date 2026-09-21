from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

from phase2_baseline import (
    CONFIG as BASE_CONFIG,
    bootstrap_terminal,
    daily_closes,
    expected_shortfall,
    first_index_price,
    load_index,
    lot_size_for_expiry,
    map_quantiles,
    net_path_pnl,
    option_intrinsic,
    read_option_entry,
    select_legs,
    strategy_ev,
    regime_features,
)


CONFIG = json.loads(Path("config/phase3_search.json").read_text(encoding="utf-8"))
RAW = Path("data/raw")
RESULTS = Path("data/derived")
RESULTS.mkdir(parents=True, exist_ok=True)


def candidate_specs() -> list[dict]:
    specs: dict[tuple[float, float, float, float], dict] = {}

    def add(family: str, values: tuple[float, float, float, float], label: str) -> None:
        key = tuple(round(v, 4) for v in values)
        if key not in specs:
            specs[key] = {
                "candidate_id": f"Q{key[0]*100:.1f}_{key[1]*100:.1f}_{key[2]*100:.1f}_{key[3]*100:.1f}".replace(".", "p").replace("-", "m"),
                "q20": key[0],
                "q35": key[1],
                "q65": key[2],
                "q80": key[3],
                "family": [family],
                "label": label,
            }
        else:
            specs[key]["family"].append(family)

    for s in CONFIG["outer_shift_points"]:
        add(
            "OUTER_SYMMETRIC",
            (0.20 - s / 100, 0.35, 0.65, 0.80 + s / 100),
            f"outer_shift_{s:+.1f}pp",
        )

    for t in CONFIG["inner_shift_points"]:
        add(
            "INNER_SYMMETRIC",
            (0.20, 0.35 - t / 100, 0.65 + t / 100, 0.80),
            f"inner_shift_{t:+.1f}pp",
        )

    for s in CONFIG["combined_shift_points"]:
        for t in CONFIG["combined_shift_points"]:
            add(
                "COMBINED_SYMMETRIC",
                (0.20 - s / 100, 0.35 - t / 100, 0.65 + t / 100, 0.80 + s / 100),
                f"outer_{s:+.1f}pp_inner_{t:+.1f}pp",
            )

    for sp in CONFIG["asymmetric_outer_shift_points"]:
        for sc in CONFIG["asymmetric_outer_shift_points"]:
            add(
                "OUTER_ASYMMETRIC",
                (0.20 - sp / 100, 0.35, 0.65, 0.80 + sc / 100),
                f"put_{sp:.1f}pp_call_{sc:.1f}pp",
            )

    return list(specs.values())


def realised_net_pnl(
    terminal_spot: float,
    legs,
    expiry: pd.Timestamp,
    lot: int,
    slippage: float,
    brokerage: float,
) -> float:
    sell_rate, exercise_rate = __import__("phase2_baseline").stt_rates(expiry)
    total = 0.0
    for leg in legs:
        adverse_entry = (
            leg.entry + slippage
            if leg.qty > 0
            else max(leg.entry - slippage, 0.0)
        )
        intrinsic = float(option_intrinsic(terminal_spot, leg.strike, leg.option_type))
        total += leg.qty * (intrinsic - adverse_entry) * lot
        if leg.qty > 0 and intrinsic > 0:
            total -= intrinsic * lot * exercise_rate
        elif leg.qty < 0:
            total -= (-leg.qty) * lot * adverse_entry * sell_rate
    total -= brokerage * len(legs)
    return float(total)


def gross_9p3_shock_loss(
    spot: float,
    legs,
    lot: int,
    shock: float,
) -> float:
    shock_spots = np.array(
        [spot * (1.0 - shock), spot * (1.0 + shock)],
        dtype=float,
    )
    pnl = strategy_ev(shock_spots, legs) * lot
    return float(max(0.0, -pnl.min()))


def build_trade_rows() -> pd.DataFrame:
    candidates = candidate_specs()
    index = load_index(RAW / "NIFTY_index.parquet")
    sensex = load_index(RAW / "SENSEX_index.parquet")
    closes = daily_closes(index)

    source_manifest = json.loads(
        (RAW / "source_manifest.json").read_text(encoding="utf-8")
    )

    rows: list[dict] = []

    for rel in source_manifest["files"]:
        path = RAW / Path(rel).name
        expiry = pd.Timestamp(path.stem)
        if expiry not in closes.index:
            continue

        ex_pos = list(closes.index).index(expiry)
        if ex_pos < 3:
            continue

        d3 = closes.index[ex_pos - 3]
        try:
            spot = first_index_price(d3, index)
            regime = regime_features(index, sensex, d3)
            prior = closes.loc[:d3].iloc[:-1]

            terminal = bootstrap_terminal(
                spot,
                prior,
                closes.index,
                d3,
                expiry,
                BASE_CONFIG["mc_paths"],
                seed=int(expiry.strftime("%Y%m%d")),
            )

            entry = read_option_entry(path, d3)
            if entry.empty:
                raise ValueError("No post-09:30 executable observations")

            lot = lot_size_for_expiry(expiry)

            for candidate in candidates:
                qvals = {
                    "P20": float(np.quantile(terminal, candidate["q20"])),
                    "P35": float(np.quantile(terminal, candidate["q35"])),
                    "P65": float(np.quantile(terminal, candidate["q65"])),
                    "P80": float(np.quantile(terminal, candidate["q80"])),
                }

                mapping = map_quantiles(qvals, entry["strike"].to_numpy(dtype=float))
                if len(set(mapping.values())) != 4:
                    raise ValueError("Unique strike mapping failed")

                legs = select_legs(mapping, entry)
                gross_paths = strategy_ev(terminal, legs)
                gross_ev = float(gross_paths.mean())
                gate = gross_ev > 0

                row = {
                    "candidate_id": candidate["candidate_id"],
                    "family": "|".join(sorted(set(candidate["family"]))),
                    "label": candidate["label"],
                    "expiry": str(expiry.date()),
                    "d3": str(d3.date()),
                    "spot_0930": spot,
                    "sensex_0930": regime["sensex_0930"],
                    "sensex_prev_close": regime["sensex_prev_close"],
                    "sensex_d3_gap_pct": regime["sensex_d3_gap_pct"],
                    "nifty_d3_gap_pct": regime["nifty_d3_gap_pct"],
                    "sensex_prior20d_log_return": regime["sensex_prior20d_log_return"],
                    "nifty_prior20d_log_return": regime["nifty_prior20d_log_return"],
                    "nifty_minus_sensex_prior20d_log_return": regime["nifty_minus_sensex_prior20d_log_return"],
                    "target_q20": candidate["q20"],
                    "target_q35": candidate["q35"],
                    "target_q65": candidate["q65"],
                    "target_q80": candidate["q80"],
                    "mapped_P20": mapping["P20"],
                    "mapped_P35": mapping["P35"],
                    "mapped_P65": mapping["P65"],
                    "mapped_P80": mapping["P80"],
                    "gross_mc_ev_points": gross_ev,
                    "gate": gate,
                    "lot_size": lot,
                    "status": "",
                    "error": "",
                }

                if gate:
                    net = net_path_pnl(
                        terminal,
                        legs,
                        expiry,
                        lot,
                        BASE_CONFIG["primary_slippage_points_per_leg"],
                        BASE_CONFIG["brokerage_per_order_inr"],
                    )
                    realised = realised_net_pnl(
                        float(closes.loc[expiry]),
                        legs,
                        expiry,
                        lot,
                        BASE_CONFIG["primary_slippage_points_per_leg"],
                        BASE_CONFIG["brokerage_per_order_inr"],
                    )
                    shock_loss = gross_9p3_shock_loss(
                        spot,
                        legs,
                        lot,
                        CONFIG["stress_spot_move"],
                    )

                    row.update(
                        {
                            "realized_net_pnl_inr": realised,
                            "win": int(realised > 0),
                            "es95_inr_proxy": expected_shortfall(-net, 0.95),
                            "es99_inr_proxy": expected_shortfall(-net, 0.99),
                            "shock9p3_gross_loss_inr": shock_loss,
                        }
                    )
                else:
                    row.update(
                        {
                            "realized_net_pnl_inr": np.nan,
                            "win": np.nan,
                            "es95_inr_proxy": expected_shortfall(-gross_paths * lot, 0.95),
                            "es99_inr_proxy": expected_shortfall(-gross_paths * lot, 0.99),
                            "shock9p3_gross_loss_inr": np.nan,
                        }
                    )

                rows.append(row)

        except Exception as exc:
            for candidate in candidates:
                rows.append(
                    {
                        "candidate_id": candidate["candidate_id"],
                        "family": "|".join(sorted(set(candidate["family"]))),
                        "label": candidate["label"],
                        "expiry": str(expiry.date()),
                        "d3": str(d3.date()),
                        "status": "SKIP",
                        "error": str(exc),
                    }
                )

    return pd.DataFrame(rows)


def summarise(trades: pd.DataFrame) -> pd.DataFrame:
    records = []

    for cid, g in trades.groupby("candidate_id", sort=False):
        valid = g[g["status"].fillna("").eq("")]
        gated = valid[valid["gate"].eq(True)]

        if len(gated):
            session_pnl = valid["realized_net_pnl_inr"].fillna(0.0)
            mean_session = float(session_pnl.mean())
            mean_gate = float(gated["realized_net_pnl_inr"].mean())
            median_gate = float(gated["realized_net_pnl_inr"].median())
            win_rate = float(gated["win"].mean())
            es95 = float(gated["es95_inr_proxy"].mean())
            es99 = float(gated["es99_inr_proxy"].mean())
            shock = float(gated["shock9p3_gross_loss_inr"].mean())
            q05 = float(gated["realized_net_pnl_inr"].quantile(0.05))
            q01 = float(gated["realized_net_pnl_inr"].quantile(0.01))
        else:
            mean_session = 0.0
            mean_gate = median_gate = win_rate = es95 = es99 = shock = q05 = q01 = np.nan

        first = valid.iloc[0] if len(valid) else g.iloc[0]
        records.append(
            {
                "candidate_id": cid,
                "family": first.get("family"),
                "label": first.get("label"),
                "target_q20": first.get("target_q20"),
                "target_q35": first.get("target_q35"),
                "target_q65": first.get("target_q65"),
                "target_q80": first.get("target_q80"),
                "valid_expiries": int(len(valid)),
                "gated_trades": int(len(gated)),
                "gate_rate": float(len(gated) / len(valid)) if len(valid) else np.nan,
                "mean_net_pnl_per_valid_expiry": mean_session,
                "mean_net_pnl_per_gated_trade": mean_gate,
                "median_net_pnl_per_gated_trade": median_gate,
                "win_rate": win_rate,
                "mean_es95_inr_proxy": es95,
                "mean_es99_inr_proxy": es99,
                "mean_shock9p3_gross_loss_inr": shock,
                "p05_realized_net_pnl_inr": q05,
                "p01_realized_net_pnl_inr": q01,
            }
        )

    out = pd.DataFrame(records)

    baseline = out[out["candidate_id"].eq(
        out.sort_values("candidate_id").iloc[0]["candidate_id"]
    )]
    # The baseline tuple is always (0.20,0.35,0.65,0.80).
    baseline = out[
        np.isclose(out["target_q20"], 0.20)
        & np.isclose(out["target_q35"], 0.35)
        & np.isclose(out["target_q65"], 0.65)
        & np.isclose(out["target_q80"], 0.80)
    ].iloc[0]

    b = trades[
        trades["candidate_id"].eq(baseline["candidate_id"])
        & trades["status"].fillna("").eq("")
    ][["expiry", "gate", "realized_net_pnl_inr", "es99_inr_proxy"]].rename(
        columns={
            "gate": "baseline_gate",
            "realized_net_pnl_inr": "baseline_pnl",
            "es99_inr_proxy": "baseline_es99",
        }
    )

    paired_rows = []
    for cid in out["candidate_id"]:
        c = trades[
            trades["candidate_id"].eq(cid)
            & trades["status"].fillna("").eq("")
        ][["expiry", "gate", "realized_net_pnl_inr", "es99_inr_proxy"]].rename(
            columns={
                "gate": "candidate_gate",
                "realized_net_pnl_inr": "candidate_pnl",
                "es99_inr_proxy": "candidate_es99",
            }
        )
        m = b.merge(c, on="expiry", how="inner")
        common = m[m["baseline_gate"].eq(True) & m["candidate_gate"].eq(True)]
        if len(common):
            delta_pnl = float((common["candidate_pnl"] - common["baseline_pnl"]).mean())
            delta_es99 = float((common["candidate_es99"] - common["baseline_es99"]).mean())
            common_n = int(len(common))
        else:
            delta_pnl = delta_es99 = np.nan
            common_n = 0
        paired_rows.append(
            {
                "candidate_id": cid,
                "common_gated_n": common_n,
                "common_gate_mean_delta_pnl_inr": delta_pnl,
                "common_gate_mean_delta_es99_inr": delta_es99,
            }
        )

    out = out.merge(pd.DataFrame(paired_rows), on="candidate_id", how="left")

    b_session = float(baseline["mean_net_pnl_per_valid_expiry"])
    b_gate = float(baseline["mean_net_pnl_per_gated_trade"])
    b_win = float(baseline["win_rate"])
    b_es99 = float(baseline["mean_es99_inr_proxy"])

    out["session_ev_retention"] = out["mean_net_pnl_per_valid_expiry"] / b_session
    out["gated_ev_retention"] = out["mean_net_pnl_per_gated_trade"] / b_gate
    out["win_delta_pp"] = (out["win_rate"] - b_win) * 100.0
    out["es99_reduction_pct"] = (1.0 - out["mean_es99_inr_proxy"] / b_es99) * 100.0
    out["shock_reduction_pct"] = (
        1.0 - out["mean_shock9p3_gross_loss_inr"] / baseline["mean_shock9p3_gross_loss_inr"]
    ) * 100.0

    frontier = []
    min_n = CONFIG["minimum_gated_trades_for_frontier"]

    for ev_tol in CONFIG["ev_tolerances"]:
        for win_tol in CONFIG["win_rate_tolerance_points"]:
            feasible = out[
                (out["gated_trades"] >= min_n)
                & (out["mean_net_pnl_per_valid_expiry"] >= b_session * (1.0 - ev_tol))
                & (out["mean_net_pnl_per_gated_trade"] >= b_gate * (1.0 - ev_tol))
                & (out["win_rate"] >= b_win - win_tol / 100.0)
            ].copy()
            feasible = feasible.sort_values(
                ["mean_es99_inr_proxy", "mean_es95_inr_proxy", "gated_trades"],
                ascending=[True, True, False],
            )
            if len(feasible):
                pick = feasible.iloc[0]
                frontier.append(
                    {
                        "ev_tolerance": ev_tol,
                        "win_rate_tolerance_pp": win_tol,
                        "candidate_id": pick["candidate_id"],
                        "label": pick["label"],
                        "mean_es99_inr_proxy": pick["mean_es99_inr_proxy"],
                        "es99_reduction_pct": pick["es99_reduction_pct"],
                        "win_rate": pick["win_rate"],
                        "mean_net_pnl_per_valid_expiry": pick["mean_net_pnl_per_valid_expiry"],
                        "mean_net_pnl_per_gated_trade": pick["mean_net_pnl_per_gated_trade"],
                        "session_ev_retention": pick["session_ev_retention"],
                        "gated_ev_retention": pick["gated_ev_retention"],
                        "win_delta_pp": pick["win_delta_pp"],
                        "gated_trades": pick["gated_trades"],
                    }
                )
            else:
                frontier.append(
                    {
                        "ev_tolerance": ev_tol,
                        "win_rate_tolerance_pp": win_tol,
                        "candidate_id": "",
                        "label": "NO_FEASIBLE_CANDIDATE",
                    }
                )

    return out.sort_values("mean_es99_inr_proxy"), pd.DataFrame(frontier)


def main() -> None:
    candidates = candidate_specs()
    Path("data/derived/phase3_candidate_universe.json").write_text(
        json.dumps(candidates, indent=2),
        encoding="utf-8",
    )

    rows = build_trade_rows()
    rows.to_csv(RESULTS / "phase3_candidate_trade_ledger.csv", index=False)

    summary, frontier = summarise(rows)
    summary.to_csv(RESULTS / "phase3_candidate_summary.csv", index=False)
    frontier.to_csv(RESULTS / "phase3_retention_frontier.csv", index=False)

    baseline = summary[
        np.isclose(summary["target_q20"], 0.20)
        & np.isclose(summary["target_q35"], 0.35)
        & np.isclose(summary["target_q65"], 0.65)
        & np.isclose(summary["target_q80"], 0.80)
    ].iloc[0]

    result = {
        "candidate_count": int(len(summary)),
        "baseline_candidate_id": baseline["candidate_id"],
        "baseline_session_ev_inr": float(baseline["mean_net_pnl_per_valid_expiry"]),
        "baseline_gated_trade_ev_inr": float(baseline["mean_net_pnl_per_gated_trade"]),
        "baseline_win_rate": float(baseline["win_rate"]),
        "baseline_mean_es99_inr": float(baseline["mean_es99_inr_proxy"]),
        "minimum_frontier_gated_trades": int(CONFIG["minimum_gated_trades_for_frontier"]),
    }
    (RESULTS / "phase3_run_summary.json").write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
