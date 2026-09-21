# MC2 — NIFTY Batman Margin-Reduction Research

Status: **Phase 2 complete provisionally; Phase 3 strike search starting**

This repository studies whether NIFTY BATMAN option strike placement can be altered to reduce margin/risk capital while retaining profit expectancy and win rate.

## Locked baseline rule

> **NIFTY BATMAN**
> - When: D3 trading session before expiry
> - Signal: 09:30 IST
> - Model: 756-session bootstrap MC, 5,000 paths
> - Gate: gross MC-EV > 0
> - Strikes: P20, P35, P65, P80 MC terminal quantiles mapped to nearest unique available strikes
> - Position: +1 P35 PE, −2 P20 PE, +1 P65 CE, −2 P80 CE
> - Execution: first executable observation after 09:30
> - Exit: expiry
> - Primary research slippage: 2 option points per execution leg
> - Costs: brokerage + STT + historical lot size
> - Sizing: ES95/ES99 risk proxy, not maximum-profit sizing

## Research status

- Phase 0 — **DONE**: repository foundation and research protocol.
- Phase 1 — **DONE**: literature, data-source, contract/cost and methodological audit.
- Phase 2 — **DONE PROVISIONALLY**: 99 expiry rows evaluated, 98 valid, 53 gross-MC-EV-gated trades, 81.13% conditional realized win rate, ₹2,442 mean realized net P&L per gated trade under the provisional MC implementation.
- Phase 3 — **IN PROGRESS**: controlled strike/spot alteration search using the same engine.
- Phase 4 — **PLANNED**: walk-forward and robustness validation.
- Phase 5 — **PLANNED**: final manuscript and reproducibility package.

## Phase 2 outputs

- [Phase 2 report](research/phase2_baseline_report.md)
- [Baseline summary](data/derived/phase2_baseline_summary.json)
- [Full baseline ledger](data/derived/phase2_baseline_trade_ledger.csv)
- [Phase 2 protocol](phase/phase2/README.md)
- [Phase 2 error log](phase/phase2/ERROR_LOG.md)

## Core methodological constraint

The research must separate:
1. economic profitability,
2. exchange/broker margin requirement,
3. a transparent risk-capital proxy when exact historical broker margin is unavailable.

The baseline rule is not to be silently changed. Any proposed alteration must be evaluated against the locked baseline under identical data, execution, cost and sizing assumptions.

## Provisional-baseline warning

The original mathematical transformation behind the phrase "756-session bootstrap MC" is not yet recovered. The current numerical baseline uses a documented bootstrap of daily log returns from the preceding 756 sessions to create terminal paths. All Phase 2/3 results are therefore labelled **provisional** until the original MC definition is recovered or otherwise established.

## Phase 3 optimisation target

Phase 3 will search a pre-registered finite family of strike perturbations. Primary outputs are:
- gross MC-EV;
- realized net EV and win rate;
- ES95/ES99;
- worst simulated loss;
- capital/risk proxy;
- relative capital reduction versus baseline.

Exact historical SPAN/broker margin, where reproducibly available, remains separate from ES proxies.

## Data policy

Official NSE/NSE Clearing sources are preferred for settlement, contract metadata, historical risk parameters, participant statistics and FII/DII activity. The validated 1-minute option source is used for the 09:30 execution reconstruction, with cross-checking and explicit coverage flags. Large or restricted raw datasets are not committed wholesale.
