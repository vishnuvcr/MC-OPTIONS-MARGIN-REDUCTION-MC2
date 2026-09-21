# Phase 2 Baseline Report

## Result status

The locked BATMAN control has now been reconstructed end-to-end using the 1-minute NIFTY option source and a reproducible provisional interpretation of the 756-session bootstrap specification.

**This is a provisional empirical baseline, not the canonical final baseline**, because the original mathematical transformation used by the strategy's 756-session Monte Carlo has not yet been recovered.

## Corrected cost convention

The locked 2-point slippage is applied directly to every entry cash flow:
- long legs execute at entry + 2 points;
- short legs execute at entry - 2 points, floored at zero.

This correction was necessary because the first implementation used slippage for the simulated path P&L but omitted its direct realized-entry impact. The first 81.13% win-rate result is therefore superseded.

## Sample and execution

- Source option files discovered: 106
- Expiry rows reaching the engine: 99
- Valid rows: 98
- Invalid row: 1, skipped because no post-09:30 executable option observation existed
- Gated trades: 53
- Gate rate among valid rows: 54.08%
- Realized wins: 41 / 53
- Realized conditional win rate: **77.36%**
- Mean realized net P&L: **₹1,702.98 per gated trade**
- Median realized net P&L: **₹2,369.68**
- Mean ES95 proxy: **₹12,209.67**
- Mean ES99 proxy: **₹12,688.27**

Historical lot sizes observed:
- 25-lot: 26 valid expiry rows
- 75-lot: 52 valid expiry rows
- 65-lot: 20 valid expiry rows

## Coverage limitation

The source manifest contains 106 NIFTY expiry files. The downloaded NIFTY index calendar did not contain seven of those expiry dates, so those files were not evaluated. No forward-fill or synthetic expiry date was used.

## Interpretation

The win rate is conditional on the gross-MC-EV gate. It should not be interpreted as an unconditional BATMAN win rate.

Mean and median net P&L include the locked 2-point-per-leg slippage convention, historical lot size, the ₹20/order brokerage scenario and date-specific STT handling.

## Model limitation

The project rule states "756-session bootstrap MC, 5,000 paths" but does not specify the mathematical path transformation. The current provisional engine uses:
1. 756 preceding NIFTY session closes;
2. daily log returns;
3. with-replacement sampling;
4. one draw per trading-session transition from D3 to expiry;
5. first post-09:30 NIFTY spot as the initial level;
6. 5,000 paths;
7. P20/P35/P65/P80 terminal-price quantiles;
8. ordered nearest-unique mapping to listed strikes.

This remains versioned as provisional.

## Phase 3 gate

The corrected baseline is suitable for controlled strike comparison. Any candidate improvement still requires Phase 4 walk-forward validation, multiple-testing-aware inference, ES95/ES99 comparison and historical SPAN/broker-margin comparison where possible.
