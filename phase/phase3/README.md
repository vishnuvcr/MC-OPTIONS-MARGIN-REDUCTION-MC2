# Phase 3 — Strike Alteration Search

Branch: phase-3-strike-search

Status: **IN PROGRESS**

## Objective

Find strike-quantile alterations that reduce risk-capital proxies while preserving the locked BATMAN economics as closely as possible.

The leg ratio remains fixed at +1, -2, +1, -2 in Phase 3 so that this phase isolates strike placement rather than mixing geometry and sizing effects.

## Candidate families

The search is finite and pre-registered:

1. Symmetric outer-wing shift: P20/P80 moved inward or outward in 0.5 percentile-point steps from -2 to +2.
2. Symmetric inner-strike shift: P35/P65 moved inward or outward in 0.5 percentile-point steps from -2 to +2.
3. Combined symmetric outer+inner shifts: a 5 x 5 grid using -2,-1,0,1,2.
4. Asymmetric outer-wing shifts: put-side and call-side outward shifts independently chosen from 0,0.5,1,1.5,2.

Percentile shifts are applied to the continuous MC terminal quantiles before the same nearest-unique-strike mapping used by the baseline.

## Primary capital proxies

1. ES95 of provisional MC terminal P&L.
2. ES99 of provisional MC terminal P&L.
3. Gross terminal loss under a +/-9.3% spot shock around the 09:30 index level.

The 9.3% shock figure is an analytical stress proxy motivated by NSE's published price-scan ceiling; it is not actual historical SPAN margin.

## Retention frontier

Because the user has not specified numeric tolerances for retain, the output reports a frontier for:
- mean gated net P&L deterioration: 0%, 2%, 5%, 10%;
- gated win-rate deterioration: 0, 1, 2, 5 percentage points.

For each cell, the candidate with the lowest ES99 proxy is identified. This is a shortlist, not a final strategy verdict.

## Statistical controls

All candidates use:
- identical D3/session universe;
- identical 756-session provisional bootstrap;
- identical 5,000 path count;
- identical 09:30 entry rule;
- identical 2-point slippage per leg;
- identical historical lot size and cost logic;
- identical expiry settlement;
- identical random seed by expiry.

The complete candidate-by-expiry table is retained so multiple-testing and paired analysis can be performed in Phase 4.
