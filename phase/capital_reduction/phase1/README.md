# Capital-Reduction Track — Phase 1

Branch: capital-reduction-phase-1
Status: IN PROGRESS — LITERATURE / MARGIN / PARAMETER AUDIT

## Objective
Translate the user's primary objective into a reproducible research specification: reduce the actual total capital/margin required to run the same one-lot BATMAN strategy by changing its parameters.

The previous MC2 research is retained intact. This is a new research track in the same repository.

## Work completed
- primary research question defined;
- capital/margin taxonomy defined;
- NSE SPAN and Paytm Money margin sources identified;
- literature matrix created;
- parameter families pre-registered;
- exclusion rules defined;
- Phase 2 input requirements documented;
- combined manuscript integration plan created.

## Key methodological decision
No position-size reduction is allowed. A parameter set that requires less capital only because fewer lots are traded is not a successful result for this study.

## Evidence informing the design
NSE states that SPAN is portfolio-based, uses scenario-based risk arrays, and incorporates portfolio netting. Paytm Money states that overnight F&O positions require complete SPAN + exposure margin and that hedge positions can reduce the overall margin requirement. These facts make complete four-leg portfolio margin modeling essential.

## Next gate
Phase 1 is complete only after the literature/data audit is documented, margin definition is fixed, parameter search space is frozen, and Phase 2 input requirements and reconciliation checks are ready.

## Next branch
capital-reduction-phase-2