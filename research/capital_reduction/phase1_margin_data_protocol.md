# Phase 1 — Margin and Capital Data Protocol

## Primary objective
Establish a reproducible definition of the actual capital required to place and carry one complete BATMAN position.

## Why the distinction matters
A four-leg strategy can have short-option margin, long-option premium cash, premium received from short legs, portfolio netting benefits, exposure margin, expiry-day additional margin, brokerage/taxes, and broker-specific funding rules. Therefore margin and cash required must not be collapsed into a single arbitrary number.

## Required historical fields
- expiry
- strike
- option type
- lot size
- quantity
- buy/sell side
- entry bid/ask/last where available
- settlement
- open interest
- traded volume
- timestamp
- underlying spot/index
- SPAN risk requirement
- exposure/extreme-loss component
- net option value treatment
- broker total upfront requirement where observable
- expiry-day additional margin
- brokerage
- STT
- exchange transaction charges where applicable
- slippage

## Primary metric hierarchy
### Tier 1 — Direct broker requirement
If an attributable historical Paytm Money margin calculation is available, store broker_total_entry_capital. This is the primary deployment-capital measure.

### Tier 2 — Reconstructed exchange requirement
If direct broker history is unavailable, reconstruct SPAN + Exposure + applicable additional margin using the historical NSE Clearing risk-parameter file for that date and the complete portfolio. Long-option premium and short-option premium cash flows are reported separately to avoid accidental double counting.

### Tier 3 — Transparent proxy
If neither direct broker nor historical SPAN reconstruction is possible, use a clearly labelled risk-capital proxy such as ES95/ES99. This is never presented as actual margin.

## Portfolio rule
The BATMAN position must be submitted to the margin model as a single combined four-leg portfolio. Modeling the legs independently and adding standalone margins would ignore the portfolio offset that SPAN explicitly supports.

## Entry vs peak capital
Store both entry_capital and peak_capital_during_holding. Expiry-day and market-stress margin can differ from D3 opening requirement.

## Candidate optimization metric
Primary: capital_reduction_pct = 1 - candidate_total_capital / baseline_total_capital. Secondary: pnl_per_capital = net_pnl / candidate_total_capital. A candidate must not be ranked purely by pnl_per_capital.

## Validation rules
1. Verify at least one known broker/example portfolio against the reconstructed calculation.
2. Use date-specific lot size.
3. Use date-specific SPAN parameters.
4. Treat expiry-day additional margin explicitly.
5. Do not forward-fill missing margin files.
6. Flag days for which exact margin cannot be reconstructed.
7. Keep separate fields for actual broker margin, reconstructed exchange margin, and proxy.

## Data-source hierarchy
1. NSE Clearing historical SPAN risk-parameter files.
2. NSE historical reports.
3. Paytm Money attributable calculator observations / archived documentation.
4. Original option-chain data sources already used by MC2.
5. Open-source mirrors only for cross-checking.

## Phase 1 deliverable
A data dictionary and executable specification sufficient to let Phase 2 calculate baseline capital requirement without changing the definition mid-study.