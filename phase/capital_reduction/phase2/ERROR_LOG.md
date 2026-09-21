# Capital-Reduction Track — Phase 2 Error Log

| ID | Date | Step | Error / limitation | Action |
|---|---|---|---|---|
| CR2-001 | 2026-09-22 | Margin data | Public documentation identifies historical SPAN files, but a stable direct historical file URL is not guaranteed by the report page. | Require a manifest with exact source filename, source URL and checksum; do not guess missing file URLs. |
| CR2-002 | 2026-09-22 | Broker equivalence | Paytm Money documentation is sufficient to define the components of upfront margin, but continuous historical broker-specific calculations are not publicly guaranteed. | Use NSE SPAN reconstruction as primary quantitative source and broker observations for reconciliation. |
| CR2-003 | 2026-09-22 | Premium accounting | SPAN net-option-value treatment and entry premium cash can otherwise be double-counted. | Report margin and premium separately and validate EntryCapital = margin_total + max(net_premium_payable, 0) against a broker/example case. |