from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


CFG = json.loads(Path("config/phase4_walk_forward.json").read_text())
SEL = Path("data/derived/phase4_training_selection.csv")
LEDGER = Path("data/derived/phase3_candidate_trade_ledger.csv")
OUT = Path("data/derived")


def main() -> None:
    sel = pd.read_csv(SEL)
    ledger = pd.read_csv(LEDGER)

    rows = []
    base_slip = 2.0
    base_brokerage = 20.0
    total_abs_qty = 6.0  # +1,-2,+1,-2

    selected_ids = set(
        sel["selected_candidate_id"].dropna().astype(str).unique()
    )
    baseline_id = "Q20p0_35p0_65p0_80p0"
    selected_ids.add(baseline_id)

    for split, gsel in sel.groupby("split", sort=False):
        for cid in sorted(selected_ids):
            g = ledger[ledger["candidate_id"].astype(str).eq(cid)].copy()
            if "window" in g.columns:
                pass
            for slippage in CFG["stress_slippage"]:
                for brokerage_multiplier in CFG["brokerage_multipliers"]:
                    delta_slip = slippage - base_slip
                    delta_brokerage = base_brokerage * brokerage_multiplier - base_brokerage
                    x = g["realized_net_pnl_inr"].astype(float).copy()

                    # Mechanical entry-cost stress. The primary ledger already
                    # contains STT; this stress layer isolates the direct
                    # slippage and brokerage delta and therefore does not claim
                    # to be a full recomputation of STT.
                    stressed = x - delta_slip * total_abs_qty * g["lot_size"].astype(float)
                    stressed = stressed - delta_brokerage * 4.0

                    rows.append(
                        {
                            "split": split,
                            "candidate_id": cid,
                            "slippage_points_per_leg": slippage,
                            "brokerage_multiplier": brokerage_multiplier,
                            "mean_pnl_per_expiry_stressed": float(np.nanmean(stressed)),
                            "median_pnl_per_expiry_stressed": float(np.nanmedian(stressed)),
                            "win_rate_stressed": float(np.nanmean(stressed > 0)),
                            "worst_pnl_stressed": float(np.nanmin(stressed)),
                            "stress_note": "Mechanical direct-entry-cost stress; not a full STT recomputation.",
                        }
                    )

    out = pd.DataFrame(rows)
    out.to_csv(OUT / "phase4_cost_stress.csv", index=False)
    print(json.dumps({"rows": int(len(out)), "selected_candidates": sorted(selected_ids)}, indent=2))


if __name__ == "__main__":
    main()
