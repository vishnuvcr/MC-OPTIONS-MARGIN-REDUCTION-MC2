# Final Provisional Research Conclusion

## Scope

This conclusion reflects the current Sensex-integrated Phase 1–5 workflow under the documented provisional 756-session MC operationalization.

## Corrected control

The Sensex-aware baseline uses 97 valid expiry observations and 52 gross-MC-EV-gated trades.

- Conditional win rate: 76.92%
- Mean net P&L / gated trade: ₹1,727.24
- Median net P&L / gated trade: ₹2,657.08
- Mean ES99 proxy: ₹12,706.60

## In-sample candidate frontier

P22/P33/P67/P78 is the strongest current in-sample ES99 frontier point:

- mean net P&L / eligible expiry: ₹1,016.80
- mean net P&L / gated trade: ₹1,730.35
- win rate: 78.95%
- ES99 proxy: ₹12,130.41
- ES99 reduction: about 4.53%

P21/P33/P67/P79 has higher in-sample economics and a smaller ES99 reduction.

## Walk-forward evidence

Two chronological training designs were tested.

### Split A

Training through 2025-06-30 selected P20.5/P35/P65/P79.5.

On the 2026 test:
- candidate: ₹2,778.75 / eligible expiry
- baseline: ₹2,907.69
- common-gated delta: -₹161.18
- 95% paired bootstrap CI: [-₹818.18, +₹334.65]
- sign-flip p=1.00

### Split B

Training through 2025-12-31 selected P22/P33/P67/P78.

On the 2026 test:
- candidate: ₹3,120.58 / eligible expiry
- baseline: ₹2,907.69
- common-gated delta: +₹266.12
- 95% paired bootstrap CI: [-₹914.74, +₹1,270.04]
- sign-flip p=0.643

The positive point estimate in Split B is not statistically established because the confidence interval crosses zero and the paired permutation test is not significant.

## Sensex findings

Sensex is useful as a cross-market diagnostic but does not provide a stable additional trading rule in the current sample. For P22/P33/P67/P78, the candidate-minus-baseline difference varied by Sensex opening-gap and NIFTY-versus-Sensex relative-return regimes, with small subgroup counts.

No Sensex-conditioned production rule is justified by the present evidence.

## Final interpretation

The research provides evidence that BATMAN strike geometry affects the empirical risk/capital profile. It does **not** establish a statistically reliable production improvement over the locked baseline.

Accordingly:

**Do not change the locked production BATMAN geometry based on the current evidence.**

The remaining high-priority scientific issue is recovery of the exact original 756-session Monte Carlo path-generation method. Re-running Phases 2–5 under the authoritative MC implementation is the next validation requirement.

## Important qualification

ES95/ES99 and stress loss are risk-capital proxies, not historical Paytm Money or exchange SPAN margin unless separately reconstructed from attributable historical margin data.
