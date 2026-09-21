from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


CONFIG = json.loads(Path("config/phase2_baseline.json").read_text())


@dataclass
class Leg:
    option_type: str
    qty: int
    strike: float
    entry: float


def lot_size_for_expiry(expiry: pd.Timestamp) -> int:
    d = expiry.date()
    if d < pd.Timestamp("2025-01-02").date():
        return 25
    if d < pd.Timestamp("2026-01-06").date():
        return 75
    return 65


def stt_rates(trade_date: pd.Timestamp) -> tuple[float, float]:
    if trade_date.date() < pd.Timestamp("2026-04-01").date():
        return 0.0010, 0.00125
    return 0.0015, 0.0015


def option_intrinsic(spot: np.ndarray | float, strike: float, option_type: str):
    if option_type == "CE":
        return np.maximum(np.asarray(spot) - strike, 0.0)
    return np.maximum(strike - np.asarray(spot), 0.0)


def map_quantiles(quantile_values: dict[str, float], available: np.ndarray) -> dict[str, float]:
    qnames = ["P20", "P35", "P65", "P80"]
    targets = np.array([quantile_values[k] for k in qnames], dtype=float)
    strikes = np.sort(np.unique(available.astype(float)))

    # Dynamic programming: ordered, distinct strikes minimizing total absolute distance.
    dp = np.full((4, len(strikes)), np.inf)
    prev = np.full((4, len(strikes)), -1, dtype=int)
    dp[0] = np.abs(strikes - targets[0])

    for i in range(1, 4):
        running_best = np.inf
        running_idx = -1
        for j in range(len(strikes)):
            k = j - 1
            if k >= 0 and dp[i - 1, k] < running_best:
                running_best = dp[i - 1, k]
                running_idx = k
            if running_idx >= 0:
                dp[i, j] = running_best + abs(strikes[j] - targets[i])
                prev[i, j] = running_idx

    j = int(np.argmin(dp[3]))
    chosen = [j]
    for i in range(3, 0, -1):
        j = prev[i, j]
        chosen.append(j)
    chosen = chosen[::-1]
    return dict(zip(qnames, strikes[chosen]))


def load_index(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path)
    df.columns = [str(c).lower() for c in df.columns]
    if "timestamp" not in df.columns:
        raise ValueError("NIFTY index parquet has no timestamp column")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"]).copy()
    if df["timestamp"].dt.tz is not None:
        df["timestamp"] = df["timestamp"].dt.tz_convert("Asia/Kolkata").dt.tz_localize(None)
    else:
        df["timestamp"] = df["timestamp"].dt.tz_localize(None)
    df["trade_date"] = df["timestamp"].dt.normalize()
    return df.sort_values("timestamp")


def first_index_price(day: pd.Timestamp, index_df: pd.DataFrame) -> float:
    x = index_df[index_df["trade_date"].eq(day) & (index_df["timestamp"].dt.time > pd.Timestamp("09:30").time())]
    if x.empty:
        raise ValueError(f"No NIFTY index bar at/after 09:30 on {day.date()}")
    return float(x.iloc[0]["open"])


def daily_closes(index_df: pd.DataFrame) -> pd.Series:
    x = (
        index_df.sort_values("timestamp")
        .groupby("trade_date", as_index=True)["close"]
        .last()
        .dropna()
    )
    return x


def regime_features(
    nifty_index: pd.DataFrame,
    sensex_index: pd.DataFrame,
    d3: pd.Timestamp,
) -> dict[str, float]:
    nifty_daily = daily_closes(nifty_index)
    sensex_daily = daily_closes(sensex_index)

    sensex_d3 = sensex_index[
        sensex_index["trade_date"].eq(d3)
        & (sensex_index["timestamp"].dt.time > pd.Timestamp("09:30").time())
    ]
    if sensex_d3.empty:
        raise ValueError(f"No Sensex post-09:30 observation on {d3.date()}")

    sensex_0930 = float(sensex_d3.iloc[0]["open"])
    prior_sensex_days = sensex_daily.loc[sensex_daily.index < d3].tail(20)
    prior_nifty_days = nifty_daily.loc[nifty_daily.index < d3].tail(20)

    sensex_prev_close = float(sensex_daily.loc[sensex_daily.index < d3].iloc[-1])
    nifty_prev_close = float(nifty_daily.loc[nifty_daily.index < d3].iloc[-1])

    sensex_20d = (
        float(np.log(prior_sensex_days.iloc[-1] / prior_sensex_days.iloc[0]))
        if len(prior_sensex_days) >= 2 else np.nan
    )
    nifty_20d = (
        float(np.log(prior_nifty_days.iloc[-1] / prior_nifty_days.iloc[0]))
        if len(prior_nifty_days) >= 2 else np.nan
    )

    return {
        "sensex_0930": sensex_0930,
        "sensex_prev_close": sensex_prev_close,
        "nifty_prev_close": nifty_prev_close,
        "sensex_d3_gap_pct": sensex_0930 / sensex_prev_close - 1.0,
        "nifty_d3_gap_pct": float(first_index_price(d3, nifty_index)) / nifty_prev_close - 1.0,
        "sensex_prior20d_log_return": sensex_20d,
        "nifty_prior20d_log_return": nifty_20d,
        "nifty_minus_sensex_prior20d_log_return": nifty_20d - sensex_20d
        if np.isfinite(nifty_20d) and np.isfinite(sensex_20d) else np.nan,
    }


def parse_expiry(path: Path) -> pd.Timestamp:
    return pd.Timestamp(path.stem)


def read_option_entry(path: Path, d3: pd.Timestamp) -> pd.DataFrame:
    cols = ["timestamp", "strike", "option_type", "open", "volume"]
    df = pd.read_parquet(path, columns=cols)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    if df["timestamp"].dt.tz is not None:
        df["timestamp"] = df["timestamp"].dt.tz_convert("Asia/Kolkata").dt.tz_localize(None)
    else:
        df["timestamp"] = df["timestamp"].dt.tz_localize(None)
    df["trade_date"] = df["timestamp"].dt.normalize()
    x = df[df["trade_date"].eq(d3) & (df["timestamp"].dt.time > pd.Timestamp("09:30").time())].copy()
    x = x.dropna(subset=["strike", "option_type", "open"])
    if "volume" in x.columns:
        x = x[x["volume"].fillna(0) > 0]
    if x.empty:
        return x
    x["option_type"] = x["option_type"].astype(str).str.upper()
    x = x.sort_values(["strike", "option_type", "timestamp"])
    return x.groupby(["strike", "option_type"], as_index=False).first()


def bootstrap_terminal(
    spot: float,
    prior_closes: pd.Series,
    trading_days: pd.Index,
    d3: pd.Timestamp,
    expiry: pd.Timestamp,
    paths: int,
    seed: int,
) -> np.ndarray:
    if len(prior_closes) < CONFIG["bootstrap_sessions"] + 1:
        raise ValueError("Insufficient history for 756-session bootstrap")
    hist = prior_closes.iloc[-(CONFIG["bootstrap_sessions"] + 1):].astype(float)
    log_returns = np.log(hist / hist.shift(1)).dropna().to_numpy()
    dates = trading_days
    try:
        d3_pos = list(dates).index(d3)
        ex_pos = list(dates).index(expiry)
    except ValueError as exc:
        raise ValueError("D3 or expiry missing from NIFTY trading calendar") from exc
    h = ex_pos - d3_pos
    if h <= 0:
        raise ValueError("Expiry must be after D3")
    rng = np.random.default_rng(seed)
    draws = rng.choice(log_returns, size=(paths, h), replace=True)
    return spot * np.exp(draws.sum(axis=1))


def strategy_ev(terminal: np.ndarray, legs: list[Leg]) -> np.ndarray:
    out = np.zeros_like(terminal, dtype=float)
    for leg in legs:
        out += leg.qty * (option_intrinsic(terminal, leg.strike, leg.option_type) - leg.entry)
    return out


def select_legs(mapping: dict[str, float], entry_df: pd.DataFrame) -> list[Leg]:
    by_key = {(float(r.strike), str(r.option_type).upper()): float(r.open) for r in entry_df.itertuples()}
    specs = [
        ("PE", 1, mapping["P35"]),
        ("PE", -2, mapping["P20"]),
        ("CE", 1, mapping["P65"]),
        ("CE", -2, mapping["P80"]),
    ]
    legs: list[Leg] = []
    for typ, qty, strike in specs:
        key = (float(strike), typ)
        if key not in by_key:
            raise ValueError(f"Missing executable leg {key}")
        legs.append(Leg(typ, qty, float(strike), by_key[key]))
    return legs


def trade_costs(legs: list[Leg], expiry: pd.Timestamp, lot: int, slippage: float, brokerage: float) -> tuple[float, float]:
    sell_rate, exercise_rate = stt_rates(expiry)
    entry_stt = 0.0
    for leg in legs:
        if leg.qty < 0:
            entry_stt += (-leg.qty) * lot * max(leg.entry - slippage, 0.0) * sell_rate
    return entry_stt + brokerage * len(legs), exercise_rate


def net_path_pnl(
    terminal: np.ndarray,
    legs: list[Leg],
    expiry: pd.Timestamp,
    lot: int,
    slippage: float,
    brokerage: float,
) -> np.ndarray:
    sell_rate, exercise_rate = stt_rates(expiry)
    out = np.zeros_like(terminal, dtype=float)
    for leg in legs:
        adverse_entry = leg.entry + slippage if leg.qty > 0 else max(leg.entry - slippage, 0.0)
        intrinsic = option_intrinsic(terminal, leg.strike, leg.option_type)
        out += leg.qty * (intrinsic - adverse_entry) * lot
        if leg.qty > 0:
            out -= np.where(intrinsic > 0, intrinsic * lot * exercise_rate, 0.0)
        elif leg.qty < 0:
            out -= (-leg.qty) * lot * max(adverse_entry, 0.0) * sell_rate
    out -= brokerage * len(legs)
    return out


def expected_shortfall(losses: np.ndarray, alpha: float) -> float:
    losses = np.asarray(losses, dtype=float)
    cutoff = np.quantile(losses, 1 - alpha)
    tail = losses[losses <= cutoff]
    if not len(tail):
        return 0.0
    return float(max(0.0, -tail.mean()))


def main() -> None:
    raw = Path("data/raw")
    index = load_index(raw / "NIFTY_index.parquet")
    sensex = load_index(raw / "SENSEX_index.parquet")
    closes = daily_closes(index)
    trading_days = list(closes.index)

    paths = CONFIG["mc_paths"]
    results = []

    for path in sorted(raw.glob("*.parquet")):
        if path.name.endswith("_index.parquet"):
            continue
        expiry = parse_expiry(path)
        if expiry not in closes.index:
            continue
        ex_pos = trading_days.index(expiry)
        if ex_pos < 3 or ex_pos < CONFIG["bootstrap_sessions"] + 1:
            continue
        d3 = trading_days[ex_pos - 3]
        try:
            spot = first_index_price(d3, index)
            regime = regime_features(index, sensex, d3)
            prior = closes.loc[:d3].iloc[:-1]
            terminal = bootstrap_terminal(
                spot, prior, closes.index, d3, expiry, paths,
                seed=int(expiry.strftime("%Y%m%d")),
            )
            entry = read_option_entry(path, d3)
            if entry.empty:
                raise ValueError("No post-09:30 executable observations")
            mapping = map_quantiles(
                {
                    "P20": float(np.quantile(terminal, 0.20)),
                    "P35": float(np.quantile(terminal, 0.35)),
                    "P65": float(np.quantile(terminal, 0.65)),
                    "P80": float(np.quantile(terminal, 0.80)),
                },
                entry["strike"].to_numpy(dtype=float),
            )
            legs = select_legs(mapping, entry)
            gross_paths = strategy_ev(terminal, legs)
            gross_ev = float(gross_paths.mean())
            if gross_ev <= 0:
                gate = False
                net = net_path_pnl(
                    terminal, legs, expiry, lot_size_for_expiry(expiry),
                    CONFIG["primary_slippage_points_per_leg"],
                    CONFIG["brokerage_per_order_inr"],
                )
                realized = float("nan")
            else:
                gate = True
                lot = lot_size_for_expiry(expiry)
                net = net_path_pnl(
                    terminal, legs, expiry, lot,
                    CONFIG["primary_slippage_points_per_leg"],
                    CONFIG["brokerage_per_order_inr"],
                )
                expiry_spot = float(closes.loc[expiry])
                # Realised expiry P&L using the same adverse entry convention as the
                # simulated path P&L. The earlier implementation omitted the
                # direct entry-price impact of the 2-point slippage assumption.
                sell_rate, exercise_rate = stt_rates(expiry)
                real_net = 0.0
                for leg in legs:
                    adverse_entry = (
                        leg.entry + CONFIG["primary_slippage_points_per_leg"]
                        if leg.qty > 0
                        else max(leg.entry - CONFIG["primary_slippage_points_per_leg"], 0.0)
                    )
                    intrinsic = float(option_intrinsic(expiry_spot, leg.strike, leg.option_type))
                    real_net += leg.qty * (intrinsic - adverse_entry) * lot
                    if leg.qty > 0 and intrinsic > 0:
                        real_net -= intrinsic * lot * exercise_rate
                    elif leg.qty < 0:
                        real_net -= (-leg.qty) * lot * adverse_entry * sell_rate
                real_net -= CONFIG["brokerage_per_order_inr"] * len(legs)
                realized = float(real_net)

            results.append(
                {
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
                    "gate": gate,
                    "P20": mapping["P20"],
                    "P35": mapping["P35"],
                    "P65": mapping["P65"],
                    "P80": mapping["P80"],
                    "premium_credit_points": -sum(l.qty * l.entry for l in legs),
                    "gross_mc_ev_points": gross_ev,
                    "realized_net_pnl_inr": realized,
                    "win": int(realized > 0) if math.isfinite(realized) else 0,
                    "es95_inr_proxy": expected_shortfall(net * -1, 0.95),
                    "es99_inr_proxy": expected_shortfall(net * -1, 0.99),
                    "lot_size": lot_size_for_expiry(expiry),
                    "data_source": "thetrademarkk/india-index-options-1m",
                    "model_status": CONFIG["model_operationalization"],
                }
            )
        except Exception as exc:
            results.append(
                {
                    "expiry": str(expiry.date()),
                    "d3": str(d3.date()),
                    "status": "SKIP",
                    "error": str(exc),
                    "data_source": "thetrademarkk/india-index-options-1m",
                }
            )

    out = pd.DataFrame(results)
    for col in ["status", "gate", "win", "realized_net_pnl_inr", "es95_inr_proxy", "es99_inr_proxy"]:
        if col not in out.columns:
            out[col] = np.nan
    out_dir = Path("data/derived")
    out_dir.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_dir / "phase2_baseline_trade_ledger.csv", index=False)

    valid = out[out["status"].isna() & out["gate"].fillna(False)]
    summary = {
        "eligible_expiries": int(len(out)),
        "gated_trades": int(len(valid)),
        "win_rate": float(valid["win"].mean()) if len(valid) else None,
        "mean_realized_net_pnl_inr": float(valid["realized_net_pnl_inr"].mean()) if len(valid) else None,
        "median_realized_net_pnl_inr": float(valid["realized_net_pnl_inr"].median()) if len(valid) else None,
        "mean_es95_inr_proxy": float(valid["es95_inr_proxy"].mean()) if len(valid) else None,
        "mean_es99_inr_proxy": float(valid["es99_inr_proxy"].mean()) if len(valid) else None,
        "model_status": CONFIG["model_operationalization"],
    }
    (out_dir / "phase2_baseline_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
