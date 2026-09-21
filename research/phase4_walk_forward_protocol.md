# Phase 4 Walk-Forward Protocol

## Primary estimand

The primary estimand is the difference between selected-candidate and baseline net P&L per eligible D3 expiry on unseen test expiries.

Secondary estimands are:
- common-gated net P&L difference;
- win-rate difference;
- ES95 and ES99 difference;
- capital-proxy reduction;
- Sensex-regime-specific differences.

## Candidate selection

Selection occurs only on the training period using the Phase 3 candidate ledger.

Selection objective:
1. enforce dual 95% profit-retention constraint;
2. enforce maximum 2 percentage-point win-rate deterioration;
3. minimize ES99 proxy.

No information from the validation/test windows enters selection.

## Sensex freeze rule

For each split:
- calculate the Sensex D3-gap median and NIFTY-minus-Sensex prior-20-session-return median on training data;
- freeze those thresholds;
- assign validation/test observations using the frozen thresholds.

## Paired bootstrap

Resample common-gated expiry observations with replacement for 10,000 replicates. Report the 2.5th and 97.5th percentiles of candidate-minus-baseline P&L.

## Paired permutation

Randomly flip the sign of each common-gated candidate-minus-baseline P&L difference. Use 10,000 permutations. Report the two-sided p-value.

## Multiple-testing disclosure

The search contains 53 candidate geometries. The final manuscript reports this search size and keeps the primary inference focused on candidates selected without using the final test period.
