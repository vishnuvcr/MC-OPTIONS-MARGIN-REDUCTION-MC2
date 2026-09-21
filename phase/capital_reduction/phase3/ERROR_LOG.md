# Capital-Reduction Track — Phase 3 Error Log

| ID | Date | Step | Error / limitation | Action |
|---|---|---|---|---|
| CR3-001 | 2026-09-22 | Capital metric | Historical SPAN files were not present in the repository cache and could not be retrieved directly through the available connector path. | Use the existing 9.3% gross stress-loss field only as an explicitly labelled interim capital-at-risk proxy. |
| CR3-002 | 2026-09-22 | Parameter coverage | Existing complete candidate outputs cover strike geometry, not all planned leg-ratio/gate variants. | Do not claim the full Phase 3 parameter space is exhausted; retain missing families for a fresh data-backed run after the margin cache is populated. |
| CR3-003 | 2026-09-22 | Ranking interpretation | The proxy is risk capital, not actual broker/exchange margin. | Keep the actual-margin acceptance gate open and carry the proxy result as exploratory only. |