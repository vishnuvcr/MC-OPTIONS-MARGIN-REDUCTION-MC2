# Phase 1 — Literature and Data Audit

Branch: phase-1-literature-data-audit

Status: **COMPLETE**

This phase establishes the literature base, official market-rule timeline, data-source hierarchy, transaction-cost timeline, and the reproducible data-acquisition design for the NIFTY BATMAN study.

## Main findings

1. Margin is not equivalent to maximum expiry loss. NSE Clearing's SPAN framework is scenario based and includes price/volatility scan ranges. Exact historical margin therefore requires historical risk parameters or an equivalent broker margin calculation.
2. Academic work supports treating margin/solvency constraints as a first-class portfolio constraint; strike placement and position limits can change implementability even when gross option strategy returns look attractive.
3. NIFTY contract mechanics changed during the study horizon. Expiry moved from Thursday to Tuesday for newly generated contracts from the 2025 transition, and NIFTY lot sizes have changed materially. The backtest must therefore use contract-specific metadata rather than a single hard-coded lot size.
4. Intraday option data is the critical bottleneck for exact reproduction of the 09:30 entry. Open datasets now exist with 1-minute NIFTY option chains, but they have partial coverage and redistribution/licensing constraints. Official daily NSE data is suitable for settlement/contract validation, but not by itself for the user's 09:30 execution rule.
5. The alteration search must control data snooping because many strike configurations can be tried on the same historical sample. Walk-forward validation and multiple-testing-aware inference are therefore mandatory.

## Phase conclusion

The research question is empirically testable, but a valid numerical result requires the derived 756-session signal/option dataset to be assembled before Phase 2. No numerical performance claim is made in this phase.
