# Combined Final Research Conclusion — MC2 + Capital Reduction

The repository now contains two linked but separately versioned research tracks.

## Original MC2 track

The Sensex-integrated original research found:
- 97 valid expiries;
- 52 gated baseline trades;
- 76.92% conditional win rate;
- ₹1,727.24 mean net P&L per gated trade;
- ES99 proxy ₹12,706.60;
- no statistically reliable production improvement from the tested strike geometries.

## New capital-reduction track

The new research restarted from Phase 1 with the explicit objective of reducing the actual total trading capital / blocked margin by changing BATMAN parameters, while keeping the one-lot scale fixed.

Because complete historical SPAN/broker margin data were not available in the working cache, the best available parameter result used a 9.3% stress-loss capital-at-risk proxy.

The training-selected P19/P35/P65/P80 geometry produced a 2026 proxy capital reduction of approximately 1.04% (₹1,195.59) on 16 common-gated observations. The paired sign-flip test gave p=0.1214. Mean gated P&L differed by -₹22.60 and the 95% paired bootstrap interval crossed zero.

## Overall conclusion

The evidence does not yet establish that a BATMAN parameter change reduces **actual NSE/Paytm Money trading margin**.

Therefore the locked production BATMAN geometry should remain unchanged.

The next scientifically required validation is:
1. acquire/cache historical NSE Clearing SPAN risk-parameter files;
2. validate the local SPAN engine against an attributable broker/reference calculation;
3. calculate actual entry and peak capital for the locked baseline;
4. rerun the complete registered strike, leg-ratio and gate parameter families;
5. repeat chronological out-of-sample validation.

The existing original MC2 research is retained intact, and the new combined manuscript integrates both tracks.
