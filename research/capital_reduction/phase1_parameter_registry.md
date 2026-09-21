# Phase 1 — Parameter Registry

The following search dimensions are pre-registered before candidate optimization.

## Fixed
- underlying: NIFTY
- position size: one historical lot per leg multiplier
- D3 timing: inherited from locked BATMAN
- baseline entry time: 09:30 IST and first executable observation convention
- expiry exit
- primary slippage: 2 option points per leg
- historical lot-size schedule
- primary transaction-cost schedule
- Sensex diagnostic alignment

## Variable family A — Strike quantiles
Baseline: (20, 35, 65, 80).
Initial grid:
- outer put: 18, 19, 20, 21, 22, 23
- inner put: 32, 33, 34, 35, 36, 37
- inner call: 63, 64, 65, 66, 67
- outer call: 77, 78, 79, 80, 81, 82
The final structured subset will be frozen before execution so the total search size remains computationally and statistically manageable.

## Variable family B — Leg ratios
Baseline absolute multipliers: (+1, -2, +1, -2). Candidate ratios must retain four legs, avoid trivial common scaling, and be pre-specified before Phase 3.

## Variable family C — Gate
Baseline: gross MC-EV > 0. Candidate thresholds will be a pre-defined set such as MC-EV > 0, MC-EV > a positive threshold, or MC-EV / capital > a specified threshold. The exact grid will be frozen before Phase 3.

## Variable family D — Strike mapping
- nearest unique listed strike
- deterministic rounding to listed strike
- collision resolution by deterministic ordered fallback

## Exclusion rules
A candidate is excluded if it changes lot count, relies on unavailable strikes without a pre-defined fallback, uses future information, changes cost assumptions during selection, cannot be compared to baseline on a common eligible sample, or is introduced after seeing test-period performance.

## Primary ranking
1. lowest actual total capital;
2. subject to profitability/win-rate constraints;
3. capital efficiency;
4. parameter stability;
5. secondary risk metrics.