# Capital-Reduction Track — Phase 4

Branch: capital-reduction-phase-4
Status: DONE PROVISIONALLY — WALK-FORWARD / CAPITAL-PROXY VALIDATION

## Candidate fixed before test
Q19 / P35 / P65 / P80 was selected using training data through 2025-12-31 only.

## 2026 test result
The candidate's gated 9.3% stress-loss capital proxy was ₹114,243 versus ₹115,439 for the baseline, a reduction of ₹1,195.59 (1.04%).

Paired bootstrap 95% CI for candidate-minus-baseline proxy capital: [-₹2,317.66, -₹286.41]. The paired sign-flip p-value was 0.1214, so the proxy reduction is not statistically established at the 5% level.

Net P&L per gated trade was ₹3,612 versus ₹3,635 baseline; paired difference -₹22.60 with 95% bootstrap CI approximately [-₹657.68, +₹818.37] and sign-flip p=1.00. Win rate was 75% for both.

## Slippage stress
At 2.5-point slippage per leg, gated-trade mean P&L was approximately ₹3,417 for the candidate versus ₹3,440 baseline. At 3 points it was approximately ₹3,222 versus ₹3,245. These are direct incremental entry-cost stresses from the six leg-units per one-lot basket.

## Interpretation
The strike change produces a small and statistically inconclusive reduction in a capital-at-risk proxy. It does not yet demonstrate a real NSE/Paytm Money margin reduction, because historical SPAN files were not available for the primary measurement.

## Next branch
capital-reduction-phase-5