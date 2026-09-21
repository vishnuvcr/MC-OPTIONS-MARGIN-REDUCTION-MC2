# Capital-Reduction Research Track — Master Plan

## Purpose

This is a new research track inside the existing MC2 repository. The previously completed Sensex-integrated BATMAN research is retained unchanged as the prior research track and remains part of the combined final manuscript.

This track starts again at Phase 1 and asks the narrower implementation question:

> Can the BATMAN strategy be parameterized so that the same one-lot four-leg position requires materially less total trading capital / blocked margin, without an unacceptable deterioration in net expectancy, win rate, or risk?

The objective is parameter-driven capital reduction, not reduction of lot count and not optimization of an ES proxy alone.

## Relationship to the previous research

The prior track remains preserved in the existing Phase 1–5 branches.

The new track carries forward the locked BATMAN execution convention, Sensex diagnostic alignment, historical lot-size treatment, transaction-cost framework, slippage assumptions, reproducibility rules, and error/status logging requirements.

The unresolved authoritative 756-session Monte Carlo transformation remains a prerequisite for any final production conclusion. It is not, however, the research question itself.

## New research question

### Primary RQ
Which admissible BATMAN parameter combination minimizes actual total capital required per complete one-lot position while preserving acceptable net expectancy, win rate, and tail-risk characteristics?

### Secondary questions
1. Which BATMAN parameters have the largest marginal effect on required margin?
2. Is capital reduction driven primarily by strike geometry, leg ratios, gating, or strike-mapping rules?
3. Can a candidate reduce margin without simply shifting risk from entry capital into larger tail losses?
4. How much capital reduction survives realistic slippage, brokerage, STT, liquidity, expiry, and volatility regimes?
5. Does the candidate remain capital-efficient out of sample?
6. Does the result persist when actual historical NSE SPAN/risk-parameter files are used instead of a risk-capital proxy?

## Primary hypotheses

H0: No admissible BATMAN parameter change produces a material reduction in actual required capital/margin while staying within pre-registered profitability and win-rate tolerances.

H1: At least one admissible parameter change materially reduces actual required capital/margin while staying within those tolerances.

## Hard constraints
1. One-lot size is fixed. Reducing the number of lots is not an allowed capital-reduction mechanism.
2. The same entry timestamp, expiry exit, and execution convention are retained unless a parameter family explicitly opens them.
3. The locked 2-point adverse slippage per leg remains the primary cost assumption.
4. Brokerage, STT and applicable transaction costs remain included.
5. Sensex is retained as a non-look-ahead robustness variable and does not silently become a signal input.
6. No candidate is accepted from in-sample performance alone.
7. A capital reduction created only by lower nominal P&L or higher tail risk is not an improvement.

## Capital definition

The research will report three separate capital quantities:

A. Exchange / broker margin: actual upfront margin blocked by NSE Clearing / broker when reproducibly available.

B. Premium cash requirement: cash needed to pay long-option premium, net of any premium received on short options, reported separately so that it is not confused with margin.

C. Total entry capital: the actual total funds that must be available to establish the complete four-leg position, using the broker/exchange definition where directly observable.

Where a direct broker total is unavailable, the reconstruction must explicitly document its formula and reconcile it against an observable broker or exchange example before being used for optimization.

ES95/ES99 remains a secondary risk diagnostic. It is not the primary capital metric.

## Primary optimization objective

Primary: minimize total entry capital / blocked margin.
Secondary: maximize net P&L per unit of required capital, subject to profitability and risk constraints.

Report absolute capital reduction in INR, percentage capital reduction, margin reduction, premium cash requirement, net P&L per eligible expiry, net P&L per gated trade, win rate, maximum loss, ES95 / ES99, capital efficiency, and sensitivity to small parameter perturbations.

## Parameter families

### Family A — Strike geometry
- Quantile grid around P20/P35/P65/P80.
- Inner-leg shifts.
- Outer-leg shifts.
- Symmetric and asymmetric wing shifts.
- Absolute strike-distance variants where liquidity and strike interval permit.

### Family B — Leg ratios
Controlled alternatives around +1 / -2 / +1 / -2. The search must exclude trivial scaling solutions such as changing the common lot multiplier.

### Family C — Gate / entry threshold
Controlled changes to the positive-MC-EV gate or other explicitly defined entry thresholds. The purpose is to test capital efficiency through selectivity, not to manufacture an artificially high return on capital by discarding most eligible trades without accounting for opportunity cost.

### Family D — Strike mapping
- nearest unique listed strike;
- deterministic rounding to listed strike;
- collision resolution by deterministic ordered fallback.

### Family E — Combined parameter designs
Only combinations already represented in the pre-registered grid may be tested. Unconstrained search after observing results is prohibited.

## Margin modeling hierarchy
1. Historical NSE Clearing SPAN risk-parameter files.
2. Reproducible broker margin calculator observations for Paytm Money.
3. Exchange/public margin documentation.
4. Transparent reconstructed margin formula.
5. ES95/ES99 and simulated worst loss only as secondary proxies when exact margin is unavailable.

The repository must never label a risk proxy as historical broker/exchange margin.

## Scientific methodology
### Phase 1
Literature, margin-system, parameter-space and data-availability audit.
### Phase 2
Baseline capital reconstruction using the locked BATMAN geometry and exact historical margin data where available.
### Phase 3
Pre-registered parameter optimization against the capital objective.
### Phase 4
Walk-forward / out-of-sample validation, regime stratification, cost stress, liquidity stress and multiple-testing adjustment.
### Phase 5
Combined manuscript integrating the original Sensex-integrated track and this capital-reduction track.

## Acceptance criteria
1. Total entry capital / blocked margin is materially lower than the locked baseline.
2. The reduction is caused by an allowed BATMAN parameter change, not by reducing the number of lots.
3. Net expectancy remains positive under the primary cost model.
4. Net P&L per gated trade and per eligible expiry remain within pre-registered tolerance bands.
5. Win-rate deterioration remains within the tolerance band.
6. The candidate survives chronological walk-forward validation.
7. Capital reduction remains directionally stable under cost/slippage stress.
8. No single expiry or regime explains the entire improvement.
9. The result is not dependent on a handful of illiquid or unavailable strikes.
10. Margin is measured using an appropriately documented exchange/broker method whenever possible.

## Statistical plan
- Descriptive statistics by candidate.
- Paired candidate-minus-baseline bootstrap confidence intervals.
- Paired sign-flip/permutation tests.
- Bootstrap confidence interval for capital reduction percentage.
- Walk-forward selection using training data only.
- Multiple-testing / selection adjustment.
- Sensitivity surface over parameter families.
- Regime-stratified capital and P&L analysis.
- Stress testing at higher slippage and cost levels.

## Research stop rule
The research stops after Phase 5 when the parameter search space has been exhausted as pre-registered, the best candidates have been validated out of sample, the final capital-reduction estimate and uncertainty interval are reported, and the combined manuscript is complete.

Further parameter expansion requires a new separately documented research track rather than silently extending this study.

## Required final answer

With the same one-lot BATMAN position and realistic NSE/Paytm Money costs and margin assumptions, what parameter set requires the least capital, how much capital does it save in rupees and percentage, and what happens to profit, win rate, and risk?