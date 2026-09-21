# Phase 1 Hypotheses for Strike/Spot Alteration

These are mechanistic hypotheses to test in Phase 3, not empirical conclusions.

## H1 — Outer-wing widening

Move the short P20 PE farther down and the short P80 CE farther up while keeping the inner long strikes unchanged.

Expected mechanism: lower exposure to extreme underlying moves and potentially lower risk-capital/margin.

Trade-off: the farther short wings may reduce collected premium or change the probability of expiry profit.

## H2 — Inner-wing widening

Move the P35 PE and P65 CE outward while keeping P20/P80 fixed.

Expected mechanism: changes the central profit region and the loss profile around the center. The direction of margin impact is ambiguous and must be measured.

## H3 — Asymmetric wing movement

NIFTY terminal distributions and option smiles are not guaranteed to be symmetric. Allow the put and call sides to move by different quantile increments.

Expected mechanism: one side may contribute disproportionate tail risk or premium, so symmetric strike movement may be inefficient.

## H4 — Limited ratio variants

Test a narrow family around the baseline 1:-2:+1:-2 structure.

Expected mechanism: reducing short quantity can lower required capital, but it also changes payoff shape and therefore is not a pure spot/strike alteration. It is a secondary research family.

## H5 — Strike-mapping effects

The mapping from a continuous MC quantile to the nearest unique listed strike can itself move the realized structure materially, particularly when strikes are sparse or several quantiles map to the same strike.

The engine must record both raw MC quantiles and the final tradable strikes and must not silently replace a collision with an arbitrary alternative.

## Primary research object

Rather than searching for a single 'best' strike set, Phase 3 will construct the empirical frontier of:

capital or margin proxy reduction
versus
net-profit retention
versus
win-rate retention
versus
tail-risk retention.

A candidate is only considered a feasible margin-reduction candidate after identical execution, cost and sizing rules are applied.
