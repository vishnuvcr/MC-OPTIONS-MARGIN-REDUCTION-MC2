# Capital-Reduction Track — Phase 1 Error Log

| ID | Date | Step | Error / limitation | Action |
|---|---|---|---|---|
| CR1-001 | 2026-09-22 | Research framing | Prior response over-emphasized recovery of the MC transformation rather than the user's primary capital-reduction objective. | Corrected the master research question and made actual total capital/margin the primary optimization target. |
| CR1-002 | 2026-09-22 | Margin definition | Margin can refer to exchange margin, broker upfront requirement, premium cash, or a risk-capital proxy. | Separated the quantities and prohibited proxy labeling as actual margin. |
| CR1-003 | 2026-09-22 | Optimization design | Reducing lot count would trivially reduce capital and would not answer the requested parameter question. | Fixed one-lot scale across the primary parameter search. |
| CR1-004 | 2026-09-22 | Data audit | Historical broker margin may not be continuously reconstructible from public documentation alone. | Use date-specific NSE SPAN reconstruction where available; keep broker-observed margin as Tier 1 where attributable. |