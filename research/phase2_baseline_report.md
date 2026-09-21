# Phase 2 Baseline Report

## Result status

The locked BATMAN control has now been reconstructed end-to-end using the 1-minute NIFTY option source and a reproducible provisional interpretation of the 756-session bootstrap specification.

**This is a provisional empirical baseline, not the canonical final baseline**, because the original mathematical transformation used by the strategy's 756-session Monte Carlo has not yet been recovered.

## Sample and execution

- Source option files discovered: 106
- Expiry rows reaching the engine: 99
- Valid rows: 98
- Invalid row: 1, skipped because no post-09:30 executable option observation existed
- Gated trades: 53
- Gate rate among all expiry rows: 53.54%
- Gate rate among valid rows: 54.08%
- Realized wins: 43 / 53
- Realized win rate: **81.13%**
- Mean realized net P&L: **₹2,442.22 per gated trade**
- Median realized net P&L: **₹3,244.48**
- Minimum realized net P&L: **−₹39,705.60**
- Maximum realized net P&L: **₹25,616.21**
- Mean ES95 proxy: **₹12,209.67**
- Mean ES99 proxy: **₹12,688.27**

Historical lot sizes observed:
- 25-lot: 26 valid expiry rows
- 75-lot: 52 valid expiry rows
- 65-lot: 20 valid expiry rows

## Coverage limitation

The source manifest contains 106 NIFTY expiry files. The downloaded NIFTY index calendar did not contain seven of those expiry dates, so those files were not evaluated. No forward-fill or synthetic expiry date was used.

## Interpretation

The 81.13% win rate is conditional on the gross-MC-EV gate. It is therefore not an unconditional BATMAN win rate.

The mean and median net P&L already include the locked 2-point-per-leg slippage convention, the historical lot-size mapping used by the engine, brokerage scenario and date-specific STT handling.

## Model limitation

The project rule states "756-session bootstrap MC, 5,000 paths" but does not specify the mathematical path transformation. The current provisional engine uses:

1. 756 preceding NIFTY session closes.
2. Daily log returns from that history.
3. With-replacement bootstrap.
4. Number of draws equal to trading-session transitions from D3 to expiry.
5. Initial level equal to the first post-09:30 NIFTY spot observation.
6. 5,000 paths.
7. P20/P35/P65/P80 terminal-price quantiles.
8. Ordered assignment to distinct listed strikes.

This implementation is versioned as provisional and will be replaced if the original MC definition is recovered.

## Phase 3 gate

The baseline is sufficiently reproducible to begin a controlled strike search, but any candidate improvement is provisional until it is tested with:
- the same MC implementation;
- paired candidate-vs-baseline comparisons;
- ES95/ES99;
- multiple-testing-aware inference;
- walk-forward validation;
- historical SPAN/broker-margin comparison where possible.
