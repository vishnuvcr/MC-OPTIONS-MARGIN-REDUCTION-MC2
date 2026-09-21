# Phase 3 Candidate Protocol

## Quantile convention

A positive outer shift s means:
- P20 target becomes 20-s
- P80 target becomes 80+s

A positive inner shift t means:
- P35 target becomes 35-t
- P65 target becomes 65+t

Negative values therefore move the corresponding pair in the opposite direction.

## Families

### Outer symmetric

(20-s, 35, 65, 80+s), s in {-2,-1.5,-1,-0.5,0,0.5,1,1.5,2}.

### Inner symmetric

(20, 35-t, 65+t, 80), t in {-2,-1.5,-1,-0.5,0,0.5,1,1.5,2}.

### Combined symmetric

(20-s,35-t,65+t,80+s), with s,t in {-2,-1,0,1,2}.

### Asymmetric outer

(20-s_put,35,65,80+s_call), with s_put and s_call independently drawn from {0,0.5,1,1.5,2}.

Duplicate parameter tuples are de-duplicated before execution.

## Feasibility

A candidate trade is valid only if:
- all four mapped strikes are distinct;
- all four options have a positive-volume observation strictly after 09:30;
- expiry settlement is available.

Candidates with gross MC-EV <= 0 are gated off, as with the locked rule.

## Comparison

Primary comparison is candidate versus baseline on common dates where both satisfy the gross-MC-EV gate.

Secondary comparison uses the candidate's own gated-trade statistics.

Capital objective is minimum ES99 subject to the retention frontier.
