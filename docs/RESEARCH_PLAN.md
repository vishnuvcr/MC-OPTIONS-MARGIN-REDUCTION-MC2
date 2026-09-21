# Research Plan — NIFTY BATMAN Spot/Strike Margin Reduction

## Research question

Can BATMAN parameters be adjusted so that the **actual total capital/trading margin required to enter and maintain one strategy position is materially reduced**, while preserving the baseline strategy's economically relevant net expectancy, win rate and acceptable risk? The primary optimization is therefore **capital/margin minimization by parameter adjustment**. ES95/ES99 is a secondary risk diagnostic, not the primary optimization target.

The parameter search may include, subject to the pre-registered search space:
- strike quantiles / strike distances;
- inner-leg and outer-leg spacing;
- leg ratios around the locked 1:-2:-2:1 structure;
- entry/gating thresholds that change which setups are traded;
- strike-rounding / nearest-unique mapping rules;
- other BATMAN parameters that directly change position construction or required capital.

The research must distinguish three separate quantities: (1) exchange/broker margin blocked, (2) cash/premium required for long-option legs, and (3) total deployable capital required for the complete four-leg position under the Paytm Money/NSE cost and margin convention.

### Primary null and alternative

- H0: No candidate alteration materially reduces capital/margin requirement without an unacceptable deterioration in net expectancy or win rate.
- H1: At least one alteration produces a meaningful reduction in capital/margin requirement while remaining within pre-specified tolerance bands for net expectancy and win rate.

## Locked baseline

NIFTY BATMAN as stated in the root README is the control arm. It must be evaluated before any candidate optimisation.

## Proposed phases

### Phase 0 — Foundation
- Create repository structure, locked-rule specification, logs, reproducibility rules, CI scaffolding.
- Status: IN PROGRESS.

### Phase 1 — Literature and data audit
- Review research on option portfolio optimisation, margin constraints, option tail risk, bootstrap/Monte Carlo inference, and Indian NIFTY option microstructure.
- Catalogue official NSE/NSE Clearing data, open datasets, and broker historical datasets.
- Resolve historical NIFTY expiry calendars, strike intervals, lot-size changes, transaction-cost regimes, and availability of 09:30+ intraday observations.
- Define a source hierarchy and data lineage.
- Deliverable: literature matrix, data dictionary, source manifest, cost/lot-size timeline.
- Status: PLANNED.

### Phase 2 — Baseline reconstruction
- Reconstruct D3-to-expiry observations.
- Add BSE SENSEX 1-minute spot alignment and non-look-ahead D3/rolling cross-market regime fields for every eligible expiry. Sensex fields are diagnostics only and do not alter the locked BATMAN signal.
- For each eligible session, map the 756-session empirical terminal sample used by the bootstrap model, generate 5,000 paths, estimate MC-EV and gate status, select P20/P35/P65/P80 and nearest unique tradable strikes.
- Apply the exact leg structure, first executable observation after 09:30, 2-point per-leg slippage, historical lot size, brokerage/STT and expiry settlement.
- Compare model decisions with realised outcomes.
- Validate missing observations, duplicated contracts, stale prices, strike collisions and expiry holidays.
- Deliverable: reproducible baseline trade ledger and quality report.
- Status: PLANNED.

### Phase 3 — Spot/strike alteration search
- Carry the same non-look-ahead Sensex regime fields into the candidate ledger.
- Report candidate performance by Sensex/NIFTY divergence and cross-market stress regimes without using Sensex to alter candidate selection.

Search only pre-specified families to avoid unconstrained data-mining:
1. Quantile grid perturbations around (20,35,65,80).
2. Symmetry-preserving and symmetry-breaking wing shifts.
3. Inner-leg spacing changes.
4. Outer-leg spacing changes.
5. Limited leg-ratio variants around (1,-2,+1,-2), subject to clearly defined payoff and margin constraints.
6. Optional strike-rounding rules when nearest-unique mapping causes collisions.

For every candidate:
- keep the same signal timing, execution convention, expiry exit, slippage, cost model and bootstrap path count;
- record gross EV, net EV, win rate, tail loss, ES95, ES99, max terminal loss, margin/risk-capital proxy, and capital efficiency;
- reject candidates that fail the gross MC-EV gate unless the study protocol explicitly creates a separate ablation arm.

Primary optimisation target:
- minimise **actual required total capital / blocked margin per complete BATMAN position**;
- subject to pre-registered tolerances on net expectancy, win rate and tail-loss behaviour;
- report absolute and percentage capital reduction versus the locked baseline;
- separately report premium cash outlay, exchange/broker margin and total deployable capital;
- use ES95/ES99 only as secondary robustness diagnostics;
- penalise parameter solutions that are fragile to strike availability, liquidity, transaction costs, expiry regime or small parameter perturbations.

Status: PLANNED.

### Phase 4 — Robustness / out-of-sample validation
- Use walk-forward splits.
- Stratify every primary robustness result by pre-entry Sensex regime and NIFTY-versus-Sensex relative-return regime.
- Freeze candidate parameters using only training data.
- Test on later unseen expiries.
- Bootstrap confidence intervals and paired tests versus baseline.
- Stress slippage above 2 points/leg, alternative cost assumptions, missing strikes, liquidity filters and expiry-event regimes.
- Report multiple-testing/selection effects.
- Compare exact historical margin where available with the transparent risk-capital proxy.
- Status: PLANNED.

### Phase 5 — Manuscript and reproducibility
- Include Sensex data lineage, cross-market regime definitions, NIFTY/Sensex divergence plots, regime-stratified results and limitations.
- Produce complete manuscript with abstract, methods, results, inference, discussion, limitations, conclusion, future work, figures, tables, appendices and supplemental data dictionary.
- Publish cached/canonical derived datasets that are legally redistributable; keep restricted-source raw data as manifests/checksums/loader instructions when redistribution is not permitted.
- Status: PLANNED.

## Acceptance criteria

A candidate may only be described as a research-supported improvement if all are true:
1. Positive net expectancy under the locked primary cost model.
2. Win rate deterioration is inside a pre-registered tolerance band.
3. **Actual required total capital / blocked margin is materially lower than baseline**, with the amount and percentage reduction explicitly reported.
4. The reduction is not created merely by reducing position size; it must arise from an allowed BATMAN parameter change or position-construction rule.
5. The improvement survives walk-forward validation.
6. Result remains directionally stable under stress slippage/cost scenarios.
7. No single expiry/regime dominates the result.

## Statistical plan

- Descriptive trade-level and regime-level statistics.
- Percentile bootstrap for EV, win rate and capital metrics.
- Paired permutation or bootstrap comparisons of candidate minus baseline.
- Confidence intervals for absolute and relative margin reduction.
- Deflated/adjusted inference for the candidate-selection process.
- Sensitivity surfaces over strike quantiles/geometry.

## Margin definition

Three layers will be reported separately:
1. **Exchange margin**: historical SPAN/risk-array or broker-calculated margin where reproducibly available.
2. **Broker margin**: Paytm Money calculation where observable and attributable to the historical date.
3. **Risk-capital proxy**: ES95/ES99, worst simulated loss, or another explicitly documented capital measure when exact historical margin is unavailable.

No proxy will be mislabeled as actual broker margin.

## Data hierarchy

Priority:
1. NSE/NSE Clearing official archives.
2. Broker historical contract data with explicit provenance.
3. Open datasets on GitHub/Hugging Face/Kaggle, used only after schema and spot-check validation.
4. Secondary commercial/history websites only as cross-checks.

Intraday execution is a distinct data requirement from daily expiry/settlement data.

## Reproducibility

Every phase branch must contain:
- a phase README,
- code/configuration used,
- data manifest/checksums,
- status update,
- error log update,
- result artifacts,
- a workflow with a manual workflow_dispatch trigger.

The research plan itself changes only when a research-plan decision changes. Routine status changes belong in STATUS_LOG.md, not by rewriting the plan.

## Cost and retention interpretation

The locked 2-option-point slippage is applied directly to the entry cash flow of every leg, not only to transaction-tax calculations. For long legs the adverse execution price is entry plus two points; for short legs it is entry minus two points, floored at zero. The same convention must be used in simulated and realised P&L.

"Retain profit" is evaluated on both:
1. net P&L per gated trade, because the rule only enters when gross MC-EV is positive; and
2. net P&L per eligible D3 expiry, because the gate frequency is part of economic performance.

A candidate must therefore satisfy the pre-registered EV tolerance on both measures before being considered feasible.

## Sensex integration

The BSE SENSEX is a required cross-market series in Phases 1–5. Phase 2 stores non-look-ahead Sensex features; Phase 3 carries them into the candidate ledger and regime tables; Phase 4 uses them for walk-forward stratification; Phase 5 reports the resulting cross-market analysis. Sensex observations never alter the locked NIFTY signal unless a separately registered cross-index ablation is explicitly opened.

Official BSE data are the preferred verification source. BSE's market-data service exposes indices OHLC data, including Sensex, and the BSE Sensex page exposes historical values. The TradeMarkk dataset provides a reproducible intraday `index/SENSEX.parquet` series with IST timestamps for the same execution-date alignment.

## Regime and market-context controls

Because the objective is to test capital efficiency rather than fit a single market regime, the final analysis will stratify results by:
- NIFTY India VIX / realised-volatility regime;
- FII/FPI and DII flow regime;
- NIFTY versus BSE Sensex relative regime and overnight global equity/volatility state;
- major global volatility/gold/FX stress state where data are available without look-ahead;
- expiry-calendar and holiday-transition regimes;
- major corporate-action/event windows that can distort index constituents or option liquidity.

These variables are **diagnostic/regime labels**, not extra signal inputs to the locked BATMAN rule. The primary strategy result remains determined only by the locked rule. Regime labels are used for robustness, heterogeneity analysis and stress attribution. Official NSE reports expose daily volatility, participant-wise open interest/trading volume, FII derivative statistics, settlements and SPAN files; the NSE FII/DII report also provides provisional combined NSE/BSE/MSEI flows.

