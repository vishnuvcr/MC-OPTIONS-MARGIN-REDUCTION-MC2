# Capital-Reduction Track — Phase 4 Error Log

| ID | Date | Step | Error / limitation | Action |
|---|---|---|---|---|
| CR4-001 | 2026-09-22 | Margin validation | Historical SPAN cache remained unavailable for quantitative 2026 margin reconstruction. | Use the pre-existing 9.3% stress-loss proxy only, and carry the actual-margin gate as unresolved. |
| CR4-002 | 2026-09-22 | Statistical inference | Test sample contains only 16 common-gated 2026 expiries. | Use paired bootstrap and sign-flip inference and report the small sample explicitly. |