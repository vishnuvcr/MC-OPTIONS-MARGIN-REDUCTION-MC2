# Phase 2 — Baseline Reconstruction

Branch: phase-2-baseline-reconstruction

Status: **DATA-CONSTRAINED / IMPLEMENTATION READY**

## Objective

Reconstruct the locked NIFTY BATMAN control strategy before testing any strike alteration.

## Required inputs

1. NIFTY 1-minute option OHLCV/OI history covering the eligible D3 sessions.
2. NIFTY spot/index history sufficient to build the 756-session bootstrap distribution.
3. BSE SENSEX 1-minute spot history for cross-market regime alignment.
3. Contract expiry and strike metadata.
5. Historical NIFTY lot-size schedule.
6. Historical transaction-tax schedule.
7. Historical brokerage scenario.
8. NSE SPAN risk-parameter files where exact exchange-margin reconstruction is attempted.

## Preferred intraday source

thetrademarkk/india-index-options-1m provides expiry-partitioned NIFTY option Parquet files beginning 27 May 2021 and continuing into 2026. The dataset card states that it contains 1-minute OHLCV(+OI) for NIFTY, BANKNIFTY and SENSEX and warns that option coverage is partial for illiquid/far strikes.

Source:
https://huggingface.co/datasets/thetrademarkk/india-index-options-1m

## Secondary intraday source

rissin/nse-options-intraday provides 1-minute NIFTY/BANKNIFTY/SENSEX history from October 2024 onward, with daily NSE bhavcopy history back to 2001.

Source:
https://huggingface.co/datasets/rissin/nse-options-intraday

It is useful for cross-checking recent observations but is not sufficient by itself for a full 756-session control history.

## Baseline reconstruction sequence

For every eligible expiry:

1. Determine D3 from the actual expiry date and historical market calendar.
2. At 09:30 IST, construct the 756-session bootstrap model using the locked project definition.
3. Generate 5,000 paths with a fixed reproducible seed scheme.
4. Calculate gross MC-EV for the baseline structure.
5. Continue only when gross MC-EV > 0.
6. Extract the P20, P35, P65 and P80 terminal-price quantiles.
7. Map each quantile to the nearest unique listed NIFTY strike.
8. Select +1 P35 PE, -2 P20 PE, +1 P65 CE and -2 P80 CE.
9. Use the first executable observation after 09:30 for each leg.
10. Apply 2 option points adverse slippage to every execution leg.
11. Hold to expiry settlement.
12. Apply historical lot size, brokerage and STT.
13. Record gross P&L, net P&L, win/loss, ES95, ES99, max loss, capital proxy and data-quality flags.
14. Store non-look-ahead Sensex fields: D3 09:30 level, previous close, D3 gap, prior-20-session return and NIFTY-minus-Sensex relative return.

## Non-negotiable validation

A trade is invalid when:
- any selected strike is absent from the source;
- unique-strike mapping fails;
- the first executable observation is unavailable;
- expiry settlement is unavailable;
- the source timestamp cannot be converted unambiguously to IST;
- the option contract metadata disagree across sources.

No forward fill across a missing entry timestamp is permitted.

## Important model specification

The repository currently contains the rule-level description "756-session bootstrap MC" but not the mathematical definition of how those 756 sessions are transformed into terminal price paths. This must be resolved from the prior BATMAN implementation or source before the numerical control result is treated as canonical. The implementation should expose the bootstrap transform as a versioned configuration rather than silently choose one.

## Output tables

- trade ledger
- data-quality report
- baseline summary
- bootstrap diagnostics
- capital-risk summary
- source reconciliation report

## Phase gate

Phase 2 is complete only when the baseline has:
- reproducible trades,
- documented coverage,
- net cost-adjusted P&L,
- win rate,
- ES95/ES99,
- and a clearly labelled margin measure or proxy.

## Sensex integration

Sensex is part of the Phase 2 data contract. It is recorded for every valid D3 but does not affect the BATMAN gate, strikes, leg ratios, execution or exit. Only information observable by 09:30 IST on D3 is permitted.

## Regime labels collected for later robustness

The baseline ledger will retain enough date information to join official regime variables after reconstruction: NIFTY volatility/India VIX, FII/FPI and DII flows, participant-wise derivative positioning, BSE Sensex/global volatility context, holiday/expiry-transition periods, and major event/corporate-action windows. These are diagnostics, not additional signal inputs.
