# Capital-Reduction Track — Phase 2

Branch: capital-reduction-phase-2
Status: DONE PROVISIONALLY — BASELINE CAPITAL RECONSTRUCTION DATA-CONSTRAINED

## Objective
Measure the locked BATMAN baseline's actual exchange-style margin and total entry-capital requirement on each eligible expiry, using date-specific SPAN risk-parameter inputs where available.

## Control
The control is the previously reconstructed one-lot BATMAN geometry, carried forward without modification. The prior track's trade ledger is copied into this branch as data/derived/prior_track_phase2_baseline_trade_ledger.csv.

## Capital components
1. SPAN margin
2. Exposure / extreme-loss component
3. Additional expiry-day or adhoc margin where applicable
4. Net option premium payable at entry
5. Brokerage/transaction costs

These components will be reported separately. No component will be silently double-counted.

## Margin timing
Because the BATMAN entry is after 09:30 IST on D3, the preferred margin input is the D3 begin-of-day SPAN file. If it is unavailable, the previous trading day's end-of-day file may be used only as a documented fallback.

Peak capital will be evaluated across the holding period when the required historical SPAN files are available. Expiry-day additional margin must be explicitly retained.

## Implementation
The baseline strikes are read from the prior trade ledger. The four-leg basket is evaluated jointly through a local SPAN engine. The primary implementation target is the daily NSE SPAN risk-parameter file; an open-source SPAN calculator is used as a reproducibility/validation aid, not as the exchange authority.

## Phase 2 acceptance gate
- historical SPAN files are mapped to D3 dates with checksums;
- at least one broker/calculator reconciliation case is documented;
- baseline entry capital is available for the maximum feasible number of gated expiries;
- missing margin files are explicitly flagged;
- entry and peak capital are separated;
- capital reduction baseline is frozen for Phase 3.

## Next branch
capital-reduction-phase-3

## Phase 2 outcome
Exact historical NSE SPAN / Paytm Money margin could not be reconstructed for the full baseline because the working cache did not contain the required historical SPAN files and the available connector path did not expose a complete historical archive. The baseline capital model, cache manifest, and local SPAN-engine interface are nevertheless frozen for a future exact-margin rerun. Phase 3 therefore used a clearly-labelled 9.3% stress-loss capital-at-risk proxy rather than claiming actual margin.
