# MC2 — NIFTY Batman Margin-Reduction Research

Status: **Phase 1 complete; Phase 2 pending data assembly**

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

- Phase 0 — **DONE**: repository foundation and research protocol.
- Phase 1 — **DONE**: literature, data-source, contract/cost and methodological audit.
- Phase 2 — **BLOCKED pending data**: baseline reconstruction requires the 09:30+ intraday option history plus historical contract/settlement data.
- Phase 3 — **PLANNED**: controlled strike/spot alteration search.
- Phase 4 — **PLANNED**: walk-forward and robustness validation.
- Phase 5 — **PLANNED**: final manuscript and reproducibility package.

## Phase 1 outputs

- [Research plan](docs/RESEARCH_PLAN.md)
- [Phase 1 report](phase/phase1/README.md)
- [Literature review](research/literature_review.md)
- [Data-source manifest](research/data_source_manifest.md)
- [Contract/cost timeline](research/contract_cost_timeline.md)
- [Strike-alteration hypotheses](research/phase1_hypotheses.md)
- [Status log](docs/STATUS_LOG.md)
- [Error log](docs/ERROR_LOG.md)
- [Conversation record](docs/CONVERSATION_LOG.md)

## Core methodological constraint

The research must separate:
1. economic profitability,
2. exchange/broker margin requirement,
3. a transparent risk-capital proxy when exact historical margin is unavailable.

The baseline rule is not to be silently changed. Any proposed alteration must be evaluated against the locked baseline under identical data, execution, cost, and sizing assumptions.

## Key Phase 1 finding

There is a defensible research basis for expecting strike geometry to affect required capital because option margining and portfolio solvency constraints depend on the combined portfolio, not just on maximum expiry payoff. However, there is no empirical result yet that a specific BATMAN alteration preserves profit and win rate.

The next numerical phase is therefore data-dependent rather than strategy-dependent.

## Data policy

Official NSE/NSE Clearing sources are preferred for settlement, contract metadata and historical risk parameters. Open 1-minute NIFTY option datasets can be used for intraday execution after schema, coverage and provenance checks. Large or restricted raw datasets should not be committed wholesale.
