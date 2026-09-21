# Combined Supplementary Tables — Capital-Reduction Research

## S1 — Original track baseline and geometry frontier

| Metric | Baseline P20/P35/P65/P80 | P22/P33/P67/P78 |
|---|---:|---:|
| Eligible expiries | 97 | 97 |
| Gated trades | 52 | 57 |
| Mean net P&L / eligible expiry | ₹925.94 | ₹1,016.80 |
| Mean net P&L / gated trade | ₹1,727.24 | ₹1,730.35 |
| Win rate | 76.92% | 78.95% |
| ES99 proxy | ₹12,706.60 | ₹12,130.41 |
| ES99 reduction | 0% | 4.53% |

## S2 — New capital-reduction training selection

| Metric | Baseline | P19/P35/P65/P80 |
|---|---:|---:|
| Training period | 2024-07 to 2025-12 | 2024-07 to 2025-12 |
| Valid expiries | 77 | 77 |
| Gated trades | 36 | 36 |
| Mean gated P&L | ₹879.52 | ₹1,003.43 |
| Win rate | 77.78% | 77.78% |
| Gated 9.3% shock proxy | ₹108,417.13 | ₹107,629.84 |
| Proxy reduction | — | ₹787.29 / 0.73% |

## S3 — New capital-reduction 2026 test

| Metric | Baseline | P19/P35/P65/P80 |
|---|---:|---:|
| Valid expiries | 20 | 20 |
| Gated trades | 16 | 16 |
| Mean gated P&L | ₹3,634.61 | ₹3,612.01 |
| Win rate | 75.00% | 75.00% |
| Gated 9.3% shock proxy | ₹115,438.77 | ₹114,243.17 |
| Proxy reduction | — | ₹1,195.59 / 1.04% |
| Paired P&L delta | — | -₹22.60 |
| P&L bootstrap 95% CI | — | [-₹657.68, +₹818.37] |
| P&L sign-flip p | — | 1.000 |
| Capital-proxy sign-flip p | — | 0.1214 |

## S4 — 2026 direct slippage-cost stress

| Slippage / leg | Baseline mean gated P&L | P19 candidate mean gated P&L |
|---:|---:|---:|
| 2.0 points | ₹3,634.61 | ₹3,612.01 |
| 2.5 points | ₹3,439.61 | ₹3,417.01 |
| 3.0 points | ₹3,244.61 | ₹3,222.01 |

## S5 — Margin measurement hierarchy

| Tier | Measurement | Interpretation |
|---|---|---|
| 1 | Attributable historical Paytm Money requirement | Preferred broker deployment capital |
| 2 | Historical NSE SPAN + exposure + additional margin | Preferred exchange-level reconstruction |
| 3 | Transparent capital-at-risk proxy | Exploratory only |

The new study's reported 1.04% reduction belongs to Tier 3, not Tier 1 or Tier 2.
