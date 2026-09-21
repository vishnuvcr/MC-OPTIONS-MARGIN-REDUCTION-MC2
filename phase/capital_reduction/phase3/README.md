# Capital-Reduction Track — Phase 3

Branch: capital-reduction-phase-3
Status: DONE PROVISIONALLY — STRIKE-GEOMETRY CAPITAL-PROXY SEARCH

## Objective
Test whether changing BATMAN strike parameters reduces required capital while retaining profitability and win rate.

## Scope actually executed
The existing 53 strike geometries from the prior MC2 search were re-ranked using the new study's capital objective. Because historical NSE SPAN files were not available in the working cache, the 9.3% gross stress-loss field was used as an interim capital-at-risk proxy.

## Selected training candidate
Q19 / P35 / P65 / P80.

## Training result
Proxy capital reduction: 0.73% (₹787.29 per gated position) with gated-trade P&L ₹1,003.43 versus ₹879.52 baseline and identical 77.78% win rate.

## Important limitation
This does not establish a real NSE/Paytm Money margin reduction. Exact historical SPAN and broker margin reconstruction remains mandatory before a production margin conclusion.

## Next branch
capital-reduction-phase-4