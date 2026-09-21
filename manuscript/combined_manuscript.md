# Combined Manuscript — MC2 NIFTY BATMAN Margin and Capital Reduction Research

## Abstract

This combined research program evaluated whether the NIFTY BATMAN option strategy can be modified to reduce the capital required to deploy the same one-lot position while retaining acceptable profitability, win rate and risk characteristics. The work was conducted as two linked research tracks in the same repository.

The first track established and stress-tested the locked BATMAN control, including a non-look-ahead BSE SENSEX diagnostic. The locked structure uses a D3-before-expiry 09:30 IST signal, a 756-session bootstrap Monte Carlo with 5,000 paths, a positive gross-MC-EV gate, P20/P35/P65/P80 strike placement, a +1/-2/+1/-2 leg ratio, first executable observation after 09:30, expiry exit, two option points of adverse slippage per leg, historical NIFTY lot sizes, brokerage and STT. The Sensex series was retained as a diagnostic regime variable and did not alter the NIFTY signal.

The first track reconstructed 97 valid Sensex-aware expiry observations and 52 gated trades. Conditional win rate was 76.92%, mean net P&L was ₹1,727.24 per gated trade, and mean ES99 proxy was ₹12,706.60. A finite 53-geometry search identified P22/P33/P67/P78 as the strongest in-sample ES99 frontier point, but chronological testing did not establish a statistically reliable production improvement.

The second track restarted from Phase 1 with a narrower primary objective: minimize actual total capital / blocked margin by changing BATMAN parameters while keeping the one-lot scale fixed. The capital study distinguished exchange margin, broker margin, premium cash requirement and risk-capital proxies. Historical NSE SPAN files and broker-observed margin were specified as the primary measurement hierarchy.

Because a complete historical SPAN cache was not available through the execution environment, the new track could not establish actual historical Paytm Money/NSE margin for every trade. Instead, a clearly labelled 9.3% spot-shock gross-loss proxy was used for a provisional parameter search and walk-forward test. Training through 2025 selected P19/P35/P65/P80. On the 2026 test period, its gated stress-capital proxy was ₹114,243 versus ₹115,439 for the locked baseline, a 1.04% reduction. A paired bootstrap 95% confidence interval for the candidate-minus-baseline proxy capital difference was approximately [-₹2,318, -₹286], but the paired sign-flip p-value was 0.1214. Net P&L per gated trade differed by only -₹22.60, with a 95% paired bootstrap interval of approximately [-₹658, +₹818], and win rate was 75% for both.

The combined conclusion is that BATMAN parameterization clearly changes capital/risk characteristics, but the present evidence does not establish a statistically reliable reduction in **actual** NSE/Paytm Money margin. The previously locked production geometry should therefore remain unchanged pending exact historical SPAN reconstruction and a full parameter search including leg-ratio and gate variants.

## 1. Introduction

The practical objective of this project is not merely to improve a risk statistic. It is to reduce the amount of capital that must be committed to a one-lot BATMAN position, while preserving acceptable economic performance.

This distinction matters because exchange and broker margin systems are portfolio based. NSE describes SPAN as a scenario-based portfolio risk system that evaluates the combined futures/options portfolio and sets margin to cover the largest reasonably expected one-day loss. NSE also states that the daily SPAN risk-parameter file contains the risk arrays and other inputs members use to calculate portfolio margin. Paytm Money describes overnight initial margin as SPAN plus exposure margin and notes that combining hedge positions can reduce overall margin; its calculator can evaluate multiple positions together.

Accordingly, the study treats the four BATMAN legs as a single portfolio and separates:
1. exchange / broker margin;
2. premium cash requirement;
3. total funds needed to establish the position;
4. risk-capital proxies used when exact margin is unavailable.

## 2. Research questions

### Track 1

Can BATMAN strike geometry be altered so that capital or risk-capital requirements fall while preserving the baseline's economically relevant profit expectancy and win rate?

### Track 2 — primary capital-reduction question

Which admissible BATMAN parameter combination minimizes the actual total capital / blocked margin required per complete one-lot position while preserving acceptable net expectancy, win rate and risk characteristics?

Secondary questions include whether the effect is driven by strike geometry, leg ratios, gating/selectivity or strike mapping, and whether any capital reduction survives unseen data and stress costs.

## 3. Locked BATMAN control

The production control remains:

- NIFTY;
- D3 trading session before expiry;
- 09:30 IST signal;
- 756-session bootstrap MC with 5,000 paths;
- gross MC-EV > 0 gate;
- terminal P20/P35/P65/P80 strike mapping;
- +1 P35 PE;
- -2 P20 PE;
- +1 P65 CE;
- -2 P80 CE;
- first executable observation strictly after 09:30;
- expiry exit;
- historical lot-size schedule;
- 2-point adverse slippage per leg;
- brokerage and STT.

The 2-point slippage is applied directly to entry cash flow: long legs execute at entry +2 points and short legs at entry -2 points, floored at zero.

The one-lot position scale is fixed for the capital-reduction search. Reducing lot count is not considered a parameter-driven margin improvement.

## 4. Data and source hierarchy

### 4.1 Intraday option/spot data

The TradeMarkk India Index & Options 1-minute dataset was used for reproducible NIFTY and SENSEX intraday alignment and option execution reconstruction. Its documentation identifies 1-minute NIFTY/BANKNIFTY/SENSEX index data, 1-minute option files and partial coverage in illiquid/far strikes. It is therefore treated as a reproducibility source rather than an unquestioned official exchange record.

### 4.2 Official NSE / NSE Clearing sources

The research hierarchy prioritizes NSE/NSE Clearing historical derivatives reports, settlement data, contract information and SPAN risk-parameter files. NSE's historical reports page explicitly exposes begin-of-day, multiple intraday and end-of-day F&O SPAN risk-parameter files. NSE Clearing's SPAN documentation states that risk arrays are supplied daily to members and used for combined portfolio margin calculation.

### 4.3 Paytm Money

Paytm Money states that overnight F&O positions require complete SPAN plus exposure margin. It also describes a margin calculator that permits multiple positions to be entered together and notes that hedge positions can reduce overall margin.

### 4.4 Marginism implementation

The open-source Marginism package was used as the reproducibility target for local parsing of NSE/NSCCL .spn files. Its documentation states that it operates directly on the exchange daily risk-parameter files and computes portfolio SPAN and exposure margin locally.

## 5. Sensex integration

Sensex is included across the original research phases as a non-look-ahead diagnostic series.

At D3 the study retained:
- first post-09:30 Sensex level;
- previous Sensex close;
- Sensex opening gap;
- prior-20-session Sensex return;
- prior-20-session NIFTY return;
- NIFTY minus Sensex relative return.

These variables are diagnostics and stratification labels, not hidden signal inputs.

## 6. Methodology

### Phase 1 — original track

The original track reviewed option portfolio optimization, option-tail-risk, margin constraints, Indian option microstructure, data availability, lot-size changes and transaction-cost regimes.

### Phase 2 — original baseline

The locked strategy was reconstructed for eligible expiries using:
- D3 identification from the trading calendar;
- provisional 756-session bootstrap;
- 5,000 Monte Carlo paths;
- gross MC-EV gate;
- tradable-strike mapping;
- first executable observation after 09:30;
- locked costs;
- expiry settlement.

### Phase 3 — original geometry search

53 unique strike geometries were evaluated. The finite search included symmetric outer shifts, inner shifts, combined shifts and limited asymmetric outer shifts.

### Phase 4 — original robustness

Two chronological walk-forward designs were used, with training-only candidate selection and 10,000-replicate paired bootstrap/sign-flip inference. Sensex regime labels were frozen from training data.

### Phase 5 — original manuscript

The complete first-track manuscript, figures and reproducibility package were assembled.

### New capital-reduction Phase 1

The second track fixed the primary optimization objective as total required capital / blocked margin rather than ES99.

### New capital-reduction Phase 2

The intended primary calculation was:
- date-specific NSE SPAN risk-parameter file;
- portfolio SPAN;
- exposure / ELM;
- additional expiry margin;
- net premium cash requirement;
- entry capital;
- peak capital.

The environment did not provide the full historical SPAN cache needed for exhaustive reconstruction. This limitation is recorded explicitly and no risk proxy is labelled as actual broker margin.

### New capital-reduction Phase 3

The complete existing 53-strike candidate output was re-ranked using the 9.3% gross spot-shock loss as an interim capital-at-risk proxy.

Candidates had to preserve:
- positive economics;
- at least 95% of baseline eligible-expiry EV;
- at least 95% of gated-trade EV;
- no more than 2 percentage points of win-rate deterioration.

### New capital-reduction Phase 4

The capital-proxy-selected candidate was frozen using training data through 31 December 2025 and tested on 2026 expiries. Paired bootstrap and sign-flip inference were performed on common-gated observations.

Additional slippage was applied mechanically from 2.0 to 2.5 and 3.0 points per leg.

### New capital-reduction Phase 5

The two tracks were integrated into a single manuscript and reproducibility package.

## 7. Results — original MC2 track

### 7.1 Baseline

| Metric | Value |
|---|---:|
| Valid expiry rows | 97 |
| Gated trades | 52 |
| Gate rate | 53.61% |
| Win rate | 76.92% |
| Mean net P&L / gated trade | ₹1,727.24 |
| Median net P&L / gated trade | ₹2,657.08 |
| Mean ES95 proxy | ₹12,234.13 |
| Mean ES99 proxy | ₹12,706.60 |
| Mean ±9.3% shock loss proxy | ₹110,577.64 |

### 7.2 In-sample geometry frontier

P22/P33/P67/P78 was the strongest in-sample ES99 frontier point:
- mean P&L / eligible expiry: ₹1,016.80;
- mean P&L / gated trade: ₹1,730.35;
- win rate: 78.95%;
- ES99 proxy: ₹12,130.41;
- ES99 reduction: approximately 4.53%.

### 7.3 Walk-forward geometry results

Split A selected P20.5/P35/P65/P79.5 and produced a 2026 common-gated P&L delta of -₹161.18, with 95% bootstrap CI [-₹818.18, +₹334.65] and sign-flip p=1.00.

Split B selected P22/P33/P67/P78 and produced a 2026 common-gated P&L delta of +₹266.12, with 95% bootstrap CI [-₹914.74, +₹1,270.04] and sign-flip p=0.643.

Neither split established a statistically reliable production improvement.

## 8. Results — new capital-reduction track

### 8.1 Training selection

The new capital objective selected:

**P19 / P35 / P65 / P80**

using training data through 31 December 2025.

Training gated capital-at-risk proxy:
- baseline: ₹108,417.13;
- candidate: ₹107,629.84;
- reduction: ₹787.29;
- reduction percentage: 0.73%.

Training gated net P&L:
- baseline: ₹879.52;
- candidate: ₹1,003.43.

Training win rate:
- baseline: 77.78%;
- candidate: 77.78%.

This satisfied the pre-registered retention screen for the available strike-geometry candidates.

### 8.2 2026 unseen test

2026 common-gated sample:

**n = 16**

Capital-at-risk proxy:
- baseline: ₹115,438.77;
- candidate: ₹114,243.17;
- reduction: ₹1,195.59;
- reduction percentage: **1.04%**.

The paired bootstrap 95% confidence interval for the candidate-minus-baseline proxy-capital difference was approximately:

**[-₹2,317.66, -₹286.41]**

The paired sign-flip p-value was:

**0.1214**

Thus, although all bootstrap differences in the sampled paired-resampling distribution remained negative, the permutation test does not establish the effect at the conventional 5% level.

### 8.3 Profitability retention

Two-point slippage:
- baseline mean P&L / gated trade: ₹3,634.61;
- candidate: ₹3,612.01;
- delta: -₹22.60.

95% paired bootstrap CI:

**[-₹657.68, +₹818.37]**

Sign-flip p-value:

**1.00**

Win rate:
- baseline: 75%;
- candidate: 75%.

The candidate therefore did not materially alter the observed win rate, but it also did not demonstrate a statistically reliable P&L improvement.

### 8.4 Slippage stress

At 2.5 points per leg:
- baseline mean gated P&L: approximately ₹3,439.61;
- candidate: approximately ₹3,417.01.

At 3.0 points per leg:
- baseline: approximately ₹3,244.61;
- candidate: approximately ₹3,222.01.

The difference remains approximately -₹22.60 because the candidate and baseline have the same one-lot six-leg-unit structure in this comparison. These are direct incremental entry-cost stresses.

## 9. Sensex robustness across the combined program

The original track found heterogeneous Sensex-regime differences. The low/high Sensex opening-gap and NIFTY-versus-Sensex relative-return partitions did not yield a stable production rule.

The new capital-reduction track retained the same regime variables but did not use them to rank the capital-proxy candidate. This preserves the separation between parameter optimization and cross-market attribution.

## 10. Margin methodology and unresolved measurement gap

This distinction is central to interpretation.

NSE SPAN is a portfolio margin framework in which the risk arrays and scenario calculations are applied jointly across the portfolio. The exchange exposes daily begin-of-day, intraday and end-of-day SPAN risk-parameter files. Paytm Money describes initial margin as SPAN plus exposure margin and also notes that combined hedge positions can reduce margin.

The new study therefore requires historical, date-specific SPAN files to answer the literal question:

> How many rupees of actual exchange/broker capital would BATMAN have required on each historical entry date?

Those files were not completely available in the working cache. Consequently:
- ES95/ES99 remains a risk-capital proxy;
- 9.3% stress loss remains a capital-at-risk proxy;
- neither is presented as historical Paytm Money margin.

The 1.04% capital-proxy reduction should therefore be treated as **exploratory evidence**, not as a verified broker-margin saving.

## 11. Discussion

The combined evidence establishes three important points.

First, BATMAN parameters do affect the capital/risk profile. Strike relocation changes the stress-loss and ES proxies even when the one-lot scale is held constant.

Second, the apparent capital benefit is small in the new capital objective. The training-selected P19/P35/P65/P80 geometry reduced the 2026 stress-capital proxy by about 1.04%, but the paired sign-flip inference did not establish a statistically reliable effect.

Third, the parameter search is not yet equivalent to a complete broker-margin optimization because exact historical SPAN inputs were unavailable and the leg-ratio/gating families were not fully re-executed in the new track.

The most important remaining technical task is therefore not another unconstrained parameter sweep. It is to obtain and cache the exact historical SPAN risk-parameter data, validate the local SPAN calculation against an attributable broker/reference case, and then rerun the same registered search with **actual capital as the objective**.

## 12. Strengths

- Existing MC2 research retained rather than overwritten;
- new track starts from Phase 1 as a distinct branch family;
- one-lot position size fixed;
- actual-margin hierarchy explicitly defined;
- Sensex retained without look-ahead;
- chronological train/test separation;
- paired bootstrap and permutation inference;
- explicit slippage stress;
- phase-level error/status logs;
- reproducibility workflows;
- combined manuscript structure.

## 13. Limitations

1. The authoritative original 756-session Monte Carlo transformation remains unresolved.
2. Complete historical SPAN files were not available in the working cache.
3. Paytm Money's historically attributable broker-level margin series is not continuously public.
4. The 2026 common-gated validation sample contains only 16 paired observations.
5. The new track's complete leg-ratio and gate-threshold search could not be executed without the missing leg-level/raw data infrastructure.
6. The 9.3% capital proxy is not equivalent to exchange or broker margin.

## 14. Conclusion

The combined research does **not** establish a production-ready parameter change.

The strongest new capital-reduction candidate found with the currently available data was:

**P19 / P35 / P65 / P80**

It reduced the 2026 gated capital-at-risk proxy by approximately **₹1,196, or 1.04%**, while maintaining the same observed 75% win rate and a nearly unchanged mean gated P&L.

However, the capital effect was not statistically established by the paired sign-flip test (p=0.1214), and, more importantly, the metric was a stress-loss proxy rather than verified NSE/Paytm Money margin.

Therefore:

**Keep the locked production BATMAN geometry unchanged.**

The correct next empirical step is to populate the repository's historical SPAN cache and rerun the registered parameter search using actual exchange/broker capital as the primary objective. Only a verified, out-of-sample reduction in actual capital should be considered a successful margin-reduction result.

## 15. Future research

1. Recover the exact authoritative 756-session MC implementation.
2. Acquire and cache historical NSE Clearing SPAN files covering all eligible D3 dates and expiry-day risk changes.
3. Validate the local SPAN engine against at least one attributable broker/calculator case.
4. Recompute actual entry and peak capital for the locked baseline.
5. Re-run the registered strike-geometry search on actual capital.
6. Execute the pending leg-ratio and gate-threshold families.
7. Add liquidity and strike-availability constraints.
8. Extend the study across Sensex, India VIX, FII/DII, global overnight markets, gold/FX stress and corporate/expiry-event regimes.
9. Perform prospective paper trading before any live implementation.

## 16. Reproducibility and repository map

Original research:
- phase-1-literature-data-audit
- phase-2-baseline-reconstruction
- phase-3-strike-search
- phase-4-walk-forward-sensex
- phase-5-manuscript-sensex

New capital-reduction research:
- capital-reduction-phase-1
- capital-reduction-phase-2
- capital-reduction-phase-3
- capital-reduction-phase-4
- capital-reduction-phase-5

Primary documents:
- docs/RESEARCH_PLAN.md
- docs/STATUS_LOG.md
- docs/ERROR_LOG.md
- research/capital_reduction/RESEARCH_PLAN.md
- research/capital_reduction/PHASE_MAP.md
- research/capital_reduction/COMBINED_MANUSCRIPT_PLAN.md
- phase-specific READMEs and error logs.

## References

1. NSE India. All Reports — Derivatives. https://www.nseindia.com/all-reports-derivatives
2. NSE Clearing. NSCCL SPAN. https://www.nseclearing.in/risk-management/equity-derivatives/nsccl-span
3. NSE India. Equity Derivatives — SPAN Risk Parameter Files. https://www.nseindia.com/static/products-services/equity-derivatives-span-risk-parameter-files
4. Paytm Money. Margin Calculator. https://www.paytmmoney.com/blog/margin-calculator/
5. Paytm Money. F&O Margin FAQ. https://www.paytmmoney.com/stocks/customer/fno-faq/margin-leverage/margin/what-is-margin-call-requirement-received-notification-email-from-paytm-money
6. Marginism. GitHub repository and documentation. https://github.com/marketcalls/marginism
7. thetrademarkk. India Index & Options 1-minute dataset. https://huggingface.co/datasets/thetrademarkk/india-index-options-1m

## Final research statement

The scientific conclusion is conservative by design:

**BATMAN parameter changes can alter capital/risk characteristics, but the current evidence does not demonstrate a statistically reliable reduction in actual trading margin/capital.**

The research therefore stops at the registered Phase 5 boundary, preserving the existing MC2 findings and identifying exact historical SPAN reconstruction plus a complete parameter search as the next scientifically necessary validation step.
