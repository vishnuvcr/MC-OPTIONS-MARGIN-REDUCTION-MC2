# Phase 3 — Capital-Reduction Candidate Search

## Optimization objective
The primary historical NSE SPAN/broker margin series is not yet cached in this environment. Therefore Phase 3 runs a clearly labelled interim capital-at-risk proxy using the existing 9.3% gross stress-loss field already calculated for every candidate/expiry.

This proxy is NOT actual broker margin. It is used only to determine whether previously tested strike geometries exhibit a directionally useful capital-reduction effect before exact SPAN files are available.

## Selection rule
Training candidates must satisfy the pre-registered retention conditions: at least 20 gated trades; eligible-expiry net P&L >= 95% of baseline; gated-trade net P&L >= 95% of baseline; win rate no more than 2 percentage points below baseline; minimize gated-trade mean 9.3% gross stress-loss proxy.

## Main result
Q19/P35/P65/P80 was selected in the 2024-2025 training period. Training proxy capital reduction was 0.73% (₹787.29 per gated position), with gated-trade net P&L ₹1,003.43 versus ₹879.52 baseline and identical 77.78% win rate.

## Limitation
This result does not establish an exchange or broker margin reduction. Exact historical SPAN and broker margin reconstruction remains mandatory before a production conclusion.