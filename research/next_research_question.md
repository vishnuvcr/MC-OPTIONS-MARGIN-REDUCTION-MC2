# Next Research Question — Parameter-Driven Capital Reduction

## Core research question

**Which admissible BATMAN parameter combination produces the lowest actual total capital requirement per complete four-leg position, while preserving economically acceptable net expectancy, win rate and risk characteristics versus the locked baseline?**

This is the primary next research question. The objective is not simply to find a lower ES95/ES99 proxy. The optimization target is the **amount of money that must actually be available/blocked to initiate and maintain the trade**.

## Parameter families

The next optimization should test pre-registered parameter families rather than unconstrained data mining:

1. **Strike-location parameters**
   - P1/P2/P3/P4 quantile locations.
   - Absolute strike distances where appropriate.
   - Symmetric and asymmetric outer/inner wing spacing.

2. **Leg-ratio parameters**
   - Controlled variants around the locked +1 / -2 / +1 / -2 construction.
   - Constraints must preserve a defined four-leg BATMAN payoff family and avoid trivial position-size scaling.

3. **Entry/gating parameters**
   - MC-EV threshold or related entry threshold.
   - Evaluate whether fewer, higher-quality trades can reduce capital usage without destroying net economics.

4. **Strike-mapping parameters**
   - Nearest-unique strike selection.
   - Rounding rules where the requested strikes collide or are unavailable.

## What must be optimized

For every candidate, calculate separately:

- total premium cash paid for long legs;
- premium cash received on short legs;
- exchange/SPAN/exposure margin attributable to short positions and offsets;
- broker-required upfront margin where Paytm Money data are available;
- total capital needed to execute the complete position;
- capital required at entry and the maximum capital/margin observed during the holding period;
- net P&L after the locked slippage, brokerage, STT and other applicable costs;
- return on capital;
- capital reduction in rupees and percentage versus baseline.

NSE describes SPAN as a portfolio-based margining system that evaluates the overall option portfolio and gives offsetting treatment to hedging positions; Paytm Money states that its option-writing margin requirement is exchange-defined and that its margin calculator reports the required upfront margin. citeturn314244search1turn314244search7

## Critical rule

**Do not reduce capital merely by reducing the number of lots.**

Lot size/position size must remain the same as the locked baseline for the primary parameter search. Otherwise the experiment would answer “what happens when we trade less,” rather than “can BATMAN be redesigned to require less capital?”

## Primary optimization metric

Primary metric:

**Capital Efficiency = Net P&L per eligible expiry / Maximum required total capital**

Secondary metrics:

- absolute capital reduction;
- percentage capital reduction;
- net P&L per gated trade;
- win rate;
- maximum loss;
- ES95/ES99;
- return on blocked margin;
- parameter stability.

## Statistical test

Each candidate will be compared with the baseline using paired, chronological data:

- absolute capital requirement difference;
- percentage capital reduction;
- net P&L difference;
- win-rate difference;
- capital-efficiency difference;
- bootstrap confidence intervals;
- paired permutation/sign-flip tests;
- walk-forward validation;
- stress testing for slippage and transaction costs.

## Decision rule

A candidate is only retained when it achieves a **material reduction in actual capital/margin** while remaining inside the pre-registered profitability and win-rate tolerances. A candidate that only reduces the ES proxy but does not reduce actual capital requirement will not satisfy the primary objective.

## Important prerequisite

The authoritative 756-session MC implementation still needs to be recovered before final production conclusions are made. The parameter-optimization research should use that authoritative implementation so that parameter selection is performed against the correct control model.

## Expected research output

The final result should answer a concrete question:

> **“With the same one-lot BATMAN position size and realistic Paytm Money/NSE execution and margin assumptions, which parameter set requires the least capital, how many rupees/% does it save, and what happens to net profit, win rate and risk?”**
