# MC2 — NIFTY Batman Margin-Reduction Research

Status: **Phases 0–5 complete provisionally; Sensex-integrated reproducibility package assembled**

This repository studies whether NIFTY BATMAN strike placement can be altered to reduce margin/risk capital while retaining profit expectancy and win rate.

## New research track: parameter-driven capital reduction

A separate research track now starts again from Phase 1 in this repository while retaining the completed Sensex-integrated MC2 research unchanged.

**Primary objective:** reduce the actual total capital / blocked margin required for the same one-lot four-leg BATMAN position by changing BATMAN parameters, not by reducing lot size.

- [Capital-reduction research plan](research/capital_reduction/RESEARCH_PLAN.md)
- [Capital-reduction phase map](research/capital_reduction/PHASE_MAP.md)
- [Phase 1 literature matrix](research/capital_reduction/phase1_literature_matrix.md)
- [Phase 1 margin/capital protocol](research/capital_reduction/phase1_margin_data_protocol.md)
- [Phase 1 parameter registry](research/capital_reduction/phase1_parameter_registry.md)
- [Combined manuscript plan](research/capital_reduction/COMBINED_MANUSCRIPT_PLAN.md)
- [Capital-reduction Phase 1 branch](https://github.com/vishnuvcr/MC-OPTIONS-MARGIN-REDUCTION-MC2/tree/capital-reduction-phase-1)
- [Capital-reduction Phase 2 branch](https://github.com/vishnuvcr/MC-OPTIONS-MARGIN-REDUCTION-MC2/tree/capital-reduction-phase-2)

## Locked baseline

- D3 trading session before expiry
- 09:30 IST
- 756-session bootstrap MC, 5,000 paths
- gross MC-EV > 0 gate
- P20 / P35 / P65 / P80 terminal quantiles
- +1 P35 PE, -2 P20 PE, +1 P65 CE, -2 P80 CE
- first executable observation after 09:30
- expiry exit
- 2 option-point adverse slippage per leg
- historical lot size, brokerage and STT

## Sensex integration

BSE SENSEX is a required cross-market diagnostic in Phases 1–5. The reproducible intraday source contains `index/SENSEX.parquet`; official BSE market-data sources remain the verification hierarchy. citeturn398533search1turn175964search0

Sensex is non-look-ahead and does not alter the locked NIFTY BATMAN signal. D3 level, previous close, opening gap, prior-20-session return and NIFTY-minus-Sensex relative return are carried into the research ledgers.

## Phase status

- **Phase 0 — DONE**
- **Phase 1 — DONE**
- **Phase 2 — DONE PROVISIONALLY:** 97 valid Sensex-aware expiry observations, 52 gated trades, 76.92% conditional win rate, ₹1,727.24 mean net P&L per gated trade, ES99 proxy ₹12,706.60.
- **Phase 3 — DONE PROVISIONALLY:** 53 finite strike geometries evaluated. P22/P33/P67/P78 reached a 4.53% in-sample ES99 reduction while retaining 100.18% of gated-trade EV and improving win rate by ~2.02pp.
- **Phase 4 — DONE PROVISIONALLY:** chronological walk-forward, paired bootstrap/permutation inference, Sensex regime stratification and cost stress completed. No statistically reliable production improvement established.
- **Phase 5 — DONE PROVISIONALLY:** full manuscript, figures, supplementary tables and data dictionary assembled.

## Final research conclusion

The finite in-sample search shows that BATMAN strike geometry materially changes the empirical risk/capital profile. However, the chronological tests do not establish a robust statistically reliable improvement over the locked control.

Split A selected P20.5/P35/P65/P79.5 and produced a -₹161 common-gated test delta with a 95% CI crossing zero and paired p=1.00.

Split B selected P22/P33/P67/P78 and produced a +₹266 common-gated test delta with a 95% CI of approximately [-₹915, +₹1,270] and paired p=0.643.

**The locked production geometry should therefore not be changed on the present evidence.**

## Main final documents

- [Final provisional research conclusion](research/final_research_conclusion.md)
- [Complete manuscript](https://github.com/vishnuvcr/MC-OPTIONS-MARGIN-REDUCTION-MC2/blob/phase-5-manuscript-sensex/manuscript/manuscript.md)
- [Phase 5 package](https://github.com/vishnuvcr/MC-OPTIONS-MARGIN-REDUCTION-MC2/tree/phase-5-manuscript-sensex/manuscript)
- [Phase 4 walk-forward branch](https://github.com/vishnuvcr/MC-OPTIONS-MARGIN-REDUCTION-MC2/tree/phase-4-walk-forward-sensex)
- [Phase 3 strike-search branch](https://github.com/vishnuvcr/MC-OPTIONS-MARGIN-REDUCTION-MC2/tree/phase-3-strike-search)
- [Phase 2 baseline branch](https://github.com/vishnuvcr/MC-OPTIONS-MARGIN-REDUCTION-MC2/tree/phase-2-baseline-reconstruction)
- [Sensex integration protocol](research/sensex_integration_protocol.md)

## Important limitation

The exact mathematical path transformation behind the project description “756-session bootstrap MC” remains unresolved. The current numerical results are therefore provisional and must be re-run under the authoritative MC implementation if recovered.

ES95/ES99 and stress-loss values are risk-capital proxies, not historical Paytm Money or exchange SPAN margin unless separately reconstructed.

## Corrected next research direction

The primary optimization target is **actual total trading capital / blocked margin**, achieved by changing admissible BATMAN parameters while keeping the one-lot position size fixed. ES95/ES99 remains a secondary risk diagnostic.

The next research question is documented in [research/next_research_question.md](research/next_research_question.md).

NSE states that SPAN is portfolio-based and gives offsetting treatment to option positions; Paytm Money states that option-writing upfront margin is exchange-defined and can be checked through its margin calculator. citeturn314244search1turn314244search7

## Future research

1. Recover the authoritative MC implementation.
2. Re-run Phases 2–5 under that exact model.
3. Reconstruct historical SPAN/broker margin directly where possible.
4. Extend official NSE/BSE cross-market history and global stress variables.
5. Test leg-ratio changes only after strike geometry is validated.
6. Conduct prospective paper trading before any live deployment.

## Capital-reduction research track — final provisional status

A second, separate Phase 1–5 research track was started in the same repository without altering the original Sensex-integrated MC2 research.

**Primary objective:** reduce actual total trading capital / blocked margin by changing BATMAN parameters while keeping one-lot position size fixed.

Status:
- Phase 1: **DONE PROVISIONALLY** — literature, margin methodology, data-source audit and parameter registry.
- Phase 2: **DONE PROVISIONALLY / DATA-CONSTRAINED** — actual historical SPAN margin cache unavailable for the full sample; local SPAN-engine interface and manifest frozen.
- Phase 3: **DONE PROVISIONALLY** — P19/P35/P65/P80 selected by training using a clearly labelled 9.3% capital-at-risk proxy.
- Phase 4: **DONE PROVISIONALLY** — 2026 test proxy reduction 1.04%, sign-flip p=0.1214; no statistically established actual-margin improvement.
- Phase 5: **DONE PROVISIONALLY** — combined manuscript and supplementary package assembled.

Key result: P19/P35/P65/P80 reduced the 2026 gated 9.3% stress-loss capital proxy by **₹1,195.59 (1.04%)** versus baseline. This is **not actual NSE/Paytm Money margin** and is therefore not a production-margin conclusion.

- [Capital-reduction research plan](research/capital_reduction/RESEARCH_PLAN.md)
- [Capital-reduction final provisional conclusion](https://github.com/vishnuvcr/MC-OPTIONS-MARGIN-REDUCTION-MC2/blob/capital-reduction-phase-5/research/capital_reduction/final_provisional_conclusion.md)
- [Combined manuscript](https://github.com/vishnuvcr/MC-OPTIONS-MARGIN-REDUCTION-MC2/blob/capital-reduction-phase-5/manuscript/combined_manuscript.md)
- [Combined final conclusion](research/combined_final_conclusion.md)
- [Combined supplementary tables](https://github.com/vishnuvcr/MC-OPTIONS-MARGIN-REDUCTION-MC2/blob/capital-reduction-phase-5/manuscript/combined_supplementary_tables.md)
- [Capital-reduction Phase 1](https://github.com/vishnuvcr/MC-OPTIONS-MARGIN-REDUCTION-MC2/tree/capital-reduction-phase-1)
- [Capital-reduction Phase 2](https://github.com/vishnuvcr/MC-OPTIONS-MARGIN-REDUCTION-MC2/tree/capital-reduction-phase-2)
- [Capital-reduction Phase 3](https://github.com/vishnuvcr/MC-OPTIONS-MARGIN-REDUCTION-MC2/tree/capital-reduction-phase-3)
- [Capital-reduction Phase 4](https://github.com/vishnuvcr/MC-OPTIONS-MARGIN-REDUCTION-MC2/tree/capital-reduction-phase-4)
- [Capital-reduction Phase 5](https://github.com/vishnuvcr/MC-OPTIONS-MARGIN-REDUCTION-MC2/tree/capital-reduction-phase-5)
