# MC2 — NIFTY Batman Margin-Reduction Research

Status: **Phase 3 complete provisionally; Sensex-integrated Phase 4 robustness now starting**

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

## Sensex integration

BSE SENSEX is now a required cross-market series in Phases 1–5. The TradeMarkk source provides `index/SENSEX.parquet` with 1-minute OHLCV and IST timestamps. Official BSE market-data/index-archive sources remain the verification hierarchy. See the BSE market-data service and BSE Sensex page listed in the research source manifest.

Sensex is recorded as a **non-look-ahead diagnostic/regime variable**. It does not alter the locked NIFTY signal, gate, strike mapping or leg ratio.

## Research status

- Phase 0 — **DONE**: repository foundation and research protocol.
- Phase 1 — **DONE**: literature, data-source, contract/cost and methodological audit; Sensex source lineage added.
- Phase 2 — **DONE PROVISIONALLY**: corrected 53 gated trades, 77.36% conditional win rate, ₹1,702.98 mean net P&L per gated trade; Sensex D3/rolling-regime fields added to the baseline ledger.
- Phase 3 — **DONE PROVISIONALLY**: 53 finite strike configurations tested under identical assumptions; Sensex fields carried into every candidate-expiry row.
- Phase 4 — **IN PROGRESS**: walk-forward, multiple-testing-aware, Sensex-stratified robustness and stress validation.
- Phase 5 — **PLANNED**: final manuscript and reproducibility package.

## Phase 2 outputs

- [Phase 2 report](research/phase2_baseline_report.md)
- [Baseline summary](data/derived/phase2_baseline_summary.json)
- [Full baseline ledger](data/derived/phase2_baseline_trade_ledger.csv)
- [Phase 2 protocol](phase/phase2/README.md)
- [Phase 2 error log](phase/phase2/ERROR_LOG.md)

## Phase 3 outputs

- [Phase 3 protocol](research/phase3_candidate_protocol.md)
- [Phase 3 candidate summary](data/derived/phase3_candidate_summary.csv)
- [Phase 3 retention frontier](data/derived/phase3_retention_frontier.csv)
- [Phase 3 candidate ledger](data/derived/phase3_candidate_trade_ledger.csv)
- [Phase 3 protocol/README](phase/phase3/README.md)

## Provisional-baseline warning

The original mathematical transformation behind the phrase "756-session bootstrap MC" is not yet recovered. The current numerical baseline uses a documented bootstrap of daily log returns from the preceding 756 sessions to create terminal paths. All Phase 2–4 results remain provisional until the original MC definition is recovered or otherwise established.

## Core methodological constraint

The research separates:
1. economic profitability,
2. exchange/broker margin requirement,
3. a transparent risk-capital proxy when exact historical margin is unavailable.

The baseline rule is not silently changed. Candidate alterations are evaluated against the locked baseline under identical data, execution, cost and sizing assumptions.

## Data policy

Official NSE/NSE Clearing and BSE sources are preferred for settlement, index history, contract metadata, historical risk parameters and participant statistics. The validated TradeMarkk 1-minute source is used for reproducible intraday execution alignment and is cross-checked against official sources where possible.
