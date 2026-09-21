# Phase 4 — Walk-Forward and Sensex-Stratified Robustness

Branch: phase-4-walk-forward-sensex

Status: **IN PROGRESS**

## Objective

Test whether the Phase 3 strike alterations survive chronological out-of-sample validation while explicitly controlling for cross-market Sensex regimes.

## Locked split design

### Split A
- Training: through 2025-06-30
- Validation: 2025-07-01 through 2025-12-31
- Test: 2026-01-01 onward

### Split B
- Training: through 2025-12-31
- Test: 2026-01-01 onward

Candidates are selected using training observations only.

## Training selection rule

A candidate must satisfy:
- >= 20 gated trades;
- mean net P&L per eligible expiry >= 95% of baseline;
- mean net P&L per gated trade >= 95% of baseline;
- win rate no more than 2 percentage points below baseline.

Among feasible candidates, select the minimum training ES99 proxy.

The baseline is always retained as the control.

## Test metrics

For the selected candidate and baseline:
- net P&L per eligible expiry;
- net P&L per gated trade;
- win rate;
- gate rate;
- ES95 / ES99;
- worst realized loss;
- 9.3% spot-shock loss proxy;
- paired candidate-minus-baseline deltas.

## Statistical inference

- Paired bootstrap CI for common-gated P&L delta.
- Paired sign-flip/permutation p-value for the common-gated P&L delta.
- Bootstrap CI for win-rate difference.
- Report candidate-universe size to quantify selection exposure.
- Do not claim significance from the training set.
- The final test estimate is the primary out-of-sample estimate.

## Sensex regime analysis

Only information available by 09:30 IST on D3 is allowed.

For each split, regime thresholds are learned from the training set:
1. Sensex D3 gap above/below the training median.
2. NIFTY minus Sensex prior-20-session return above/below the training median.

The selected candidate and baseline are then compared within each frozen test regime.

These regime labels are diagnostics; they never alter candidate selection in Phase 4.

## Stress matrix

Re-evaluate the selected candidate and baseline at:
- 2.0 point slippage per leg;
- 2.5 point slippage per leg;
- 3.0 point slippage per leg;
- ±25% and ±50% brokerage;
- conservative STT scenario;
- liquidity-filtered observations where positive volume is required.

Exact historical SPAN/broker margin remains a separate layer from the ES proxy.

## Phase gate

Phase 4 is complete only when:
- both chronological splits have been evaluated;
- candidate selection is training-only;
- test metrics and paired inference are reproducible;
- Sensex-stratified test results are reported;
- stress scenarios are reported;
- no final production recommendation is made while the original 756-session MC transformation remains unresolved.
