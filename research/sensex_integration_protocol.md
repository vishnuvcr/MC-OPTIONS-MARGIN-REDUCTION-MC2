# Sensex Integration Protocol

## Purpose

Add the BSE SENSEX as a first-class cross-market context series without changing the locked NIFTY BATMAN control signal.

## Source hierarchy

1. BSE official market-data / index archive sources.
   - BSE market-data service exposes Indices OHLC data for the Sensex and other indices.
   - BSE's Sensex page exposes historical values and current OHLC fields.
2. TradeMarkk 1-minute index dataset for reproducible intraday alignment:
   - `index/SENSEX.parquet`
   - IST timestamps
   - OHLCV schema
3. Cross-check against independent sources where coverage permits.

## Phase usage

### Phase 1 — audit

Document:
- BSE Sensex definition and source lineage;
- historical holiday/session alignment;
- timezone;
- missing-session treatment;
- cross-market interpretation.

### Phase 2 — baseline

For every D3:
- Sensex first executable post-09:30 observation;
- previous Sensex close;
- D3 open gap;
- prior 20-session Sensex log return;
- corresponding NIFTY values;
- NIFTY minus Sensex prior-20-session relative return.

These variables are stored in the baseline ledger but do **not** alter the gate, strikes or position sizing.

### Phase 3 — candidate search

The same Sensex fields are attached to every candidate-by-expiry row.

Candidate performance is additionally summarized by:
- high/low Sensex D3 gap;
- positive/negative prior-20-session relative return;
- high/low NIFTY-vs-Sensex divergence;
- joint high-volatility and cross-market stress buckets where available.

Sensex remains a diagnostic variable, not an optimization input.

### Phase 4 — walk-forward robustness

Sensex regime labels are frozen using information available by D3 and are used for:
- stratified candidate-vs-baseline comparisons;
- heterogeneity analysis;
- stress-state analysis;
- robustness checks for 2025 and 2026 holdout periods.

No future Sensex observations may enter candidate selection.

### Phase 5 — manuscript

The final manuscript will include:
- Sensex source/data lineage;
- cross-market regime definitions;
- Sensex/NIFTY correlation and divergence tables;
- performance by Sensex regime;
- limitations from different exchange calendars and source coverage.

## Non-look-ahead rule

Only Sensex information observable by 09:30 IST on the D3 decision date may be used in any regime label. Expiry-day or post-entry Sensex information is never permitted in signal construction or candidate selection.
