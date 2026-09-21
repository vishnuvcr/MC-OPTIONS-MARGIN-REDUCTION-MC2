# MC2 — NIFTY Batman Margin-Reduction Research

Status: **Phase 0 — repository foundation**

This repository studies whether NIFTY BATMAN option strike placement can be altered to reduce margin/risk capital while retaining profit expectancy and win rate.

## Locked baseline rule

> **NIFTY BATMAN**
> - When: D3 trading session before expiry
> - Signal: 09:30 IST
> - Model: 756-session bootstrap MC, 5,000 paths
> - Gate: gross MC-EV > 0
> - Strikes: P20, P35, P65, P80 MC terminal quantiles mapped to nearest unique available strikes
> - Position: +1 P35 PE, −2 P20 PE, +1 P65 CE, −2 P80 CE
> - Execution: first executable observation after 09:30
> - Exit: expiry
> - Primary research slippage: 2 option points per execution leg
> - Costs: brokerage + STT + historical lot size
> - Sizing: ES95/ES99 risk proxy, not maximum-profit sizing

## Research status

- Phase 0 — **In progress**: repository foundation and research protocol.
- Phase 1 — **Planned**: literature, data-source, rule and cost audit.
- Phase 2 — **Planned**: baseline reconstruction and data-quality validation.
- Phase 3 — **Planned**: strike alteration search with margin objective.
- Phase 4 — **Planned**: out-of-sample validation and robustness.
- Phase 5 — **Planned**: final manuscript and reproducible package.

## Key project files

- [Research plan](docs/RESEARCH_PLAN.md)
- [Decision/status log](docs/STATUS_LOG.md)
- [Error log](docs/ERROR_LOG.md)
- [Conversation record](docs/CONVERSATION_LOG.md)

## Core methodological constraint

The research must separate:
1. economic profitability,
2. exchange/broker margin requirement,
3. a transparent risk-capital proxy when exact historical broker margin is unavailable.

The baseline rule is not to be silently changed. Any proposed alteration must be evaluated against the locked baseline under identical data, execution, cost, and sizing assumptions.

## Sources

Primary and secondary sources are documented in the research files. The intended data hierarchy is official NSE/NSE Clearing where feasible, supplemented by clearly attributed open datasets and broker datasets for intraday validation.
