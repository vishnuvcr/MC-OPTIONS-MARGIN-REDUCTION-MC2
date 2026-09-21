# Capital-Reduction Track — Final Provisional Conclusion

## Primary answer

The best capital-reduction candidate found with the currently available data was:

**P19 / P35 / P65 / P80**

It was selected using only training data through 31 December 2025.

## 2026 test

On 16 common-gated 2026 expiries:

- baseline stress-capital proxy: ₹115,438.77;
- candidate stress-capital proxy: ₹114,243.17;
- reduction: ₹1,195.59;
- reduction: 1.04%;
- paired bootstrap 95% CI for difference: [-₹2,317.66, -₹286.41];
- sign-flip p=0.1214.

Mean gated net P&L was ₹3,634.61 for the baseline and ₹3,612.01 for the candidate, a difference of -₹22.60 with 95% paired bootstrap CI approximately [-₹657.68, +₹818.37]. Both had a 75% win rate.

## Interpretation

The strike change produces a small exploratory reduction in a stress-loss capital proxy, but the effect is not statistically established by the paired sign-flip test.

More importantly, the proxy is not actual historical NSE or Paytm Money margin. Therefore this result does **not** yet demonstrate that P19/P35/P65/P80 reduces the actual trading amount/capital blocked by the broker.

## Production decision

Do not change the locked production BATMAN geometry on this evidence.

## Required next empirical validation

Populate the historical SPAN cache, validate the local SPAN engine against an attributable broker/calculator case, compute actual entry and peak capital, and rerun the registered geometry, leg-ratio and gate parameter families.

