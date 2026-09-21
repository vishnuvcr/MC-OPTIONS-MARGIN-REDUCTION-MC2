# Phase 2 — Baseline Capital Calculation Method

## Portfolio definition
The baseline position is:
- +1 P35 put
- -2 P20 put
- +1 P65 call
- -2 P80 call

All quantities are one historical lot multiplied by the fixed leg ratio.

## Margin engine
NSE SPAN is a portfolio-based scenario margin methodology. The four legs are therefore passed as one portfolio, preserving internal offsets.

## Capital calculations
Let M = SPAN + exposure + applicable additional margin.

Let P = net option premium cash requirement at entry, where positive P denotes a net premium payment and negative P denotes a net premium receipt.

Primary reconstructed entry funds requirement:
EntryCapital = M + max(P, 0)

The formula is deliberately kept separate from net premium receipt because the SPAN calculation itself accounts for net option value. The implementation must validate this convention against an attributable broker calculator before being treated as broker-equivalent.

## Secondary measures
- Margin-only requirement = M
- Net premium cashflow = -P
- Entry capital = M + max(P, 0)
- Peak capital = maximum observed total across the holding period
- Capital efficiency = realized net P&L / peak capital

## Validation
At least one known portfolio must be reconciled against a broker or independently documented calculator example. Differences must be logged rather than normalized away.