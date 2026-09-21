from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(".")
DERIVED = ROOT / "data" / "derived"
OUT = ROOT / "manuscript"
FIG = OUT / "figures"
OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)


def load_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(DERIVED / name)


def main() -> None:
    p2 = json.loads((DERIVED / "phase2_baseline_summary.json").read_text())
    p3 = load_csv("phase3_candidate_summary.csv")
    p4 = load_csv("phase4_walk_forward_results.csv") if (DERIVED / "phase4_walk_forward_results.csv").exists() else pd.DataFrame()
    p4r = load_csv("phase4_sensex_regime_results.csv") if (DERIVED / "phase4_sensex_regime_results.csv").exists() else pd.DataFrame()
    stress = load_csv("phase4_cost_stress.csv") if (DERIVED / "phase4_cost_stress.csv").exists() else pd.DataFrame()

    baseline = p3[
        (p3["target_q20"].round(6) == 0.20)
        & (p3["target_q35"].round(6) == 0.35)
        & (p3["target_q65"].round(6) == 0.65)
        & (p3["target_q80"].round(6) == 0.80)
    ].iloc[0]

    selected = None
    if (DERIVED / "phase4_training_selection.csv").exists():
        sel = load_csv("phase4_training_selection.csv")
        picked = sel[sel["candidate_id"] == sel["selected_candidate_id"]]
        if len(picked):
            selected = picked.sort_values("split").iloc[0]["selected_candidate_id"]

    # Figure 1: Phase 3 ES99 versus EV retention.
    plt.figure(figsize=(8, 5))
    plt.scatter(
        p3["gated_ev_retention"] * 100,
        p3["mean_es99_inr_proxy"],
        s=20,
    )
    plt.axvline(95, linestyle="--")
    plt.xlabel("Gated-trade EV retention (%)")
    plt.ylabel("Mean ES99 proxy (₹)")
    plt.title("Phase 3 candidate capital-risk frontier")
    plt.tight_layout()
    plt.savefig(FIG / "phase3_es99_frontier.png", dpi=180)
    plt.close()

    # Figure 2: candidate versus baseline on walk-forward tests.
    if len(p4):
        x = p4["split"].astype(str) + " / " + p4["period_role"].astype(str)
        plt.figure(figsize=(9, 5))
        plt.plot(x, p4["candidate_mean_pnl_per_expiry"], marker="o", label="selected candidate")
        plt.plot(x, p4["baseline_mean_pnl_per_expiry"], marker="o", label="baseline")
        plt.xticks(rotation=35, ha="right")
        plt.ylabel("Net P&L / eligible expiry (₹)")
        plt.title("Walk-forward net P&L")
        plt.legend()
        plt.tight_layout()
        plt.savefig(FIG / "walk_forward_pnl.png", dpi=180)
        plt.close()

    # Figure 3: Sensex regime deltas.
    if len(p4r):
        z = p4r.dropna(subset=["mean_delta_pnl"]).copy()
        plt.figure(figsize=(9, 5))
        labels = z["regime_field"].astype(str) + " / " + z["regime"].astype(str)
        plt.bar(labels, z["mean_delta_pnl"])
        plt.xticks(rotation=35, ha="right")
        plt.ylabel("Candidate - baseline P&L (₹)")
        plt.title("Sensex-stratified common-gated P&L difference")
        plt.tight_layout()
        plt.savefig(FIG / "sensex_regime_delta.png", dpi=180)
        plt.close()

    stress_text = "Cost-stress results unavailable." if not len(stress) else (
        f"Cost-stress table contains {len(stress)} scenario rows."
    )

    md = f"""# NIFTY BATMAN Margin-Reduction Research

## Abstract

This study evaluates whether pre-specified changes to the NIFTY BATMAN strike geometry can reduce risk-capital proxies while preserving the strategy's economic characteristics after slippage, brokerage, STT and historical lot-size treatment. The study uses a provisional 756-session bootstrap Monte Carlo implementation because the original mathematical transformation underlying the project description has not yet been recovered.

The study also integrates BSE SENSEX as a non-look-ahead cross-market diagnostic in all phases.

## Research question

Can the locked P20/P35/P65/P80 BATMAN strike locations be altered to reduce capital/risk while retaining net expectancy and win rate under realistic execution costs?

## Methods

### Locked baseline

- D3 before expiry
- 09:30 IST decision
- 756-session bootstrap
- 5,000 paths
- positive gross MC-EV gate
- +1 P35 PE, -2 P20 PE, +1 P65 CE, -2 P80 CE
- first executable observation after 09:30
- 2-point adverse slippage per leg
- historical lot-size mapping
- brokerage and STT
- expiry settlement

### Sensex integration

Sensex is sourced from the reproducible 1-minute index dataset and cross-checked against official BSE source hierarchy. Only information available by 09:30 IST is used for regime labels:
- D3 Sensex level;
- previous close;
- D3 opening gap;
- prior-20-session Sensex return;
- NIFTY minus Sensex prior-20-session relative return.

Sensex never changes the locked NIFTY BATMAN signal.

## Phase 2 baseline

- Eligible expiry rows: {p2.get("eligible_expiries")}
- Gross-MC-EV-gated trades: {p2.get("gated_trades")}
- Conditional win rate: {p2.get("win_rate", float("nan")):.2%}
- Mean net P&L / gated trade: ₹{p2.get("mean_realized_net_pnl_inr", float("nan")):,.2f}
- Median net P&L / gated trade: ₹{p2.get("median_realized_net_pnl_inr", float("nan")):,.2f}
- Mean ES99 proxy: ₹{p2.get("mean_es99_inr_proxy", float("nan")):,.2f}

## Phase 3 candidate search

The finite search evaluated {len(p3)} unique quantile geometries. Candidate feasibility required retention of both per-expiry and per-gated-trade economics plus a win-rate tolerance.

The baseline row recorded:
- mean P&L / eligible expiry: ₹{baseline["mean_net_pnl_per_valid_expiry"]:,.2f}
- mean P&L / gated trade: ₹{baseline["mean_net_pnl_per_gated_trade"]:,.2f}
- win rate: {baseline["win_rate"]:.2%}
- ES99 proxy: ₹{baseline["mean_es99_inr_proxy"]:,.2f}

Selected candidate entering Phase 4: **{selected if selected else "not yet selected"}**

![Phase 3 ES99 frontier](figures/phase3_es99_frontier.png)

## Phase 4 walk-forward

The primary out-of-sample estimand is selected-candidate minus baseline net P&L per eligible D3 expiry.

{p4.to_markdown(index=False) if len(p4) else "Walk-forward results pending."}

![Walk-forward P&L](figures/walk_forward_pnl.png)

## Sensex-stratified robustness

{p4r.to_markdown(index=False) if len(p4r) else "Sensex-stratified results pending."}

![Sensex regime P&L differences](figures/sensex_regime_delta.png)

## Cost stress

{stress_text}

{stress.to_markdown(index=False) if len(stress) else ""}

## Statistical analysis

Paired bootstrap confidence intervals and paired sign-flip permutation tests are applied to common-gated candidate-minus-baseline expiry differences. Candidate selection is performed on training data only. The final test windows are not used for candidate selection.

## Results interpretation

The evidence should be interpreted as provisional because:
1. the exact original 756-session Monte Carlo path transformation is not recovered;
2. the intraday option source has partial coverage in illiquid/far strikes;
3. Sensex availability reduces the usable sample by one expiry in the current source window;
4. exact historical broker/SPAN margin is not reconstructed for every observation;
5. candidate search creates a multiple-comparison/selection burden.

## Strengths

- locked baseline control;
- deterministic seed by expiry;
- explicit transaction-cost treatment;
- historical lot-size mapping;
- finite pre-registered candidate grid;
- chronological out-of-sample testing;
- Sensex cross-market diagnostics;
- complete candidate-level ledger.

## Limitations

The provisional MC operationalization is the main limitation. The risk-capital layer is also partly proxy-based where exact historical margin is unavailable. The source dataset is not an official exchange feed and requires cross-validation.

## Conclusion

The research can support a candidate geometry only if it survives the pre-specified walk-forward and cost-stress criteria while remaining robust across Sensex regimes. No production change should be treated as final until the original MC transformation and exact historical margin methodology are resolved.

## Future research

1. Recover or reconstruct the original MC transformation from the strategy's authoritative implementation.
2. Replace proxy risk capital with historical SPAN/broker margin where possible.
3. Extend official BSE/NSE cross-market history and include additional global stress variables.
4. Test leg-ratio alterations only after strike geometry is validated.
5. Conduct a prospective paper-trading period before any production deployment.

## Reproducibility

All code, phase configurations, error logs, workflows and derived tables are stored in the repository. Sensex source lineage is documented in `research/sensex_integration_protocol.md`.
"""
    (OUT / "manuscript.md").write_text(md, encoding="utf-8")
    print("manuscript generated")


if __name__ == "__main__":
    main()
