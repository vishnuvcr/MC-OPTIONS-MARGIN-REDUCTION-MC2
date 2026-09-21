# Status Log

| Step | Phase | Status | Outcome |
|---|---|---|---|
| 0.1 | Foundation | DONE | Repository initialized and locked rule recorded. |
| 0.1a | Foundation | DONE | Research plan, status and error logs created. |
| 1.1 | Literature/data | DONE | Literature and data-source audit completed. |
| 1.2 | Literature/data | DONE | NSE/NSE Clearing, intraday datasets and open-source ingestion references catalogued. |
| 1.3 | Literature/data | DONE | Expiry, lot-size and transaction-cost regimes documented. |
| 1.4 | Literature/data | DONE | Strike/spot alteration hypotheses documented. |
| 1.5 | Literature/data | DONE | Sensex/BSE source lineage and non-look-ahead cross-market protocol added. |
| 2.1 | Baseline reconstruction | DONE PROVISIONALLY | Corrected 5,000-path baseline reconstructed with explicit 2-point entry slippage, costs and Sensex diagnostics. |
| 2.2 | Baseline reconstruction | DONE PROVISIONALLY | 99 expiry rows reached the engine; 97 valid after Sensex D3 availability; 52 gated trades. |
| 2.3 | Baseline reconstruction | DONE PROVISIONALLY | 76.92% conditional win rate; ₹1,727.24 mean net P&L/gated trade; ES99 proxy ₹12,706.60. |
| 3.1 | Strike alteration search | DONE PROVISIONALLY | 53 finite strike configurations evaluated under identical provisional MC/cost/execution assumptions. |
| 3.2 | Strike alteration search | DONE PROVISIONALLY | P22/P33/P67/P78 was the current in-sample ES99 frontier point (~4.53% ES99 reduction). |
| 4.1 | Walk-forward robustness | DONE PROVISIONALLY | Two chronological split designs evaluated with training-only candidate selection. |
| 4.2 | Sensex robustness | DONE PROVISIONALLY | Sensex D3-gap and NIFTY-vs-Sensex relative-return stratifications completed; subgroup counts remain small. |
| 4.3 | Cost stress | DONE PROVISIONALLY | 2.0/2.5/3.0 point slippage and brokerage multiplier stress completed as a mechanical direct-entry-cost diagnostic. |
| 5.1 | Manuscript | DONE PROVISIONALLY | Complete manuscript, figures, supplementary tables and data dictionary assembled on phase-5-manuscript-sensex. |
| 5.2 | Final conclusion | DONE PROVISIONALLY | No statistically reliable production improvement established over the locked baseline. |
| 5.3 | Reproducibility | DONE PROVISIONALLY | Manual workflows are complete; the final manuscript package, figures, supplementary tables and data dictionary are committed. The temporary canary trigger was removed after the parser correction; canary runs are not treated as research evidence. |

| 6.0 | Research direction | CORRECTED | Primary objective reconfirmed: reduce actual total trading capital/margin by changing BATMAN parameters, not merely reduce an ES/risk proxy. Next research question recorded in `research/next_research_question.md`. |

| CR-1.0 | Capital-reduction research | STARTED | New independent Phase 1–5 research track added in the same repository; prior Sensex-integrated Phases 0–5 retained. Primary target is parameter-driven actual capital/margin reduction. |
| CR-1.1 | Capital-reduction Phase 1 | DONE PROVISIONALLY | Literature, margin methodology, data-source matrix, parameter registry, and combined manuscript plan completed. |
| CR-2.1 | Capital-reduction Phase 2 | IN PROGRESS | Baseline capital reconstruction branch created; prior trade ledger carried forward; SPAN cache/manifest and margin calculation engine specification committed. |

| CR-2.2 | Capital-reduction Phase 2 | DONE PROVISIONALLY / DATA-CONSTRAINED | Baseline margin model and SPAN cache manifest frozen; exact historical SPAN/broker data unavailable for full-sample calculation. |
| CR-3.1 | Capital-reduction Phase 3 | DONE PROVISIONALLY | P19/P35/P65/P80 selected on 2024-2025 training using 9.3% stress-loss capital proxy; 0.73% training proxy reduction. |
| CR-4.1 | Capital-reduction Phase 4 | DONE PROVISIONALLY | 2026 common-gated test proxy reduction 1.04%; paired sign-flip p=0.1214; P&L delta -₹22.60 with CI crossing zero. |
| CR-5.1 | Capital-reduction Phase 5 | DONE PROVISIONALLY | Combined manuscript, supplementary tables, data dictionary, figures and final provisional conclusion assembled. |
