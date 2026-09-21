# Literature Review

## Option portfolio optimisation and margin

Guasoni, Mayerhofer and Zhao (2026), "Options portfolio selection with position limits", studies index-option portfolio choice under trading frictions, position limits and margin-like solvency constraints. The study treats capital constraints as an implementation issue rather than an afterthought.

Cont et al., "Counter-cyclical Margins for Option Portfolios", studies how option portfolios can be decomposed into simple strategies so that margin netting can be improved. The key implication for this project is that portfolio composition can affect margin even when payoff exposure looks similar.

## NIFTY option tail risk

"The impact of COVID-19 on tail risk: Evidence from Nifty index options" uses NIFTY option prices to study volatility smiles, risk-neutral density, skewness and kurtosis. This supports keeping historical terminal outcomes and option-implied distributions as separate concepts.

## Bootstrap and dependence

Politis and Romano (1994), "The Stationary Bootstrap", provides a resampling approach for weakly dependent stationary observations. The project keeps the user-specified 756-session bootstrap as the locked control and uses dependence-aware resampling as a robustness check.

## Data snooping and multiple testing

White (2000), "A Reality Check for Data Snooping", addresses the risk of selecting apparently good models after repeated reuse of the same historical sample.

Hansen (2005), "A Test for Superior Predictive Ability", develops a related framework for comparing many alternatives.

Bailey and Lopez de Prado (2014), "The Deflated Sharpe Ratio", addresses selection bias, non-normality and backtest overfitting.

The project consequence is that Phase 3 must pre-register candidate families, retain the full candidate search universe, and use out-of-sample validation.

## Exchange margin mechanics

NSE Clearing's SPAN documentation describes scenario-based risk parameters, including price-scan and volatility-scan components. Exact historical exchange margin therefore requires date-specific risk parameters and portfolio scenarios.

## Practitioner material

Two NIFTY butterfly/iron-butterfly videos were found and will be used only as qualitative context. Practitioner material is not treated as evidence for the empirical conclusion.

## Synthesis

The reviewed literature supports an explicit margin/capital objective, systematic strike-geometry testing, careful resampling, and multiple-testing controls.

None of the reviewed sources establishes that the exact NIFTY BATMAN rule is optimal. That remains an empirical question.
