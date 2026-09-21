# Error Log

| ID | Date | Phase | Error / limitation | Action |
|---|---|---|---|---|
| ERR-001 | 2026-09-22 | Foundation | Repository was empty; no prior files, plan, results or data were available. | Treat as clean initialization; do not invent prior history. |
| ERR-002 | 2026-09-22 | Foundation | Direct container network access to Hugging Face failed with DNS resolution error. | Do not claim local dataset download. Use web metadata and reproducible ingestion instructions instead. |
| ERR-003 | 2026-09-22 | Phase 1 | Some GitHub connector writes for code/workflow artifacts were rejected. | Keep accepted research artifacts authoritative and do not claim rejected files exist. |
| ERR-004 | 2026-09-22 | Phase 2 | First successful numerical canary revealed an expiry-calendar bug: expiry lookup was performed inside a pre-D3 history slice, causing valid expiries to be marked unavailable. | Corrected the bootstrap calendar lookup to use the full trading calendar while keeping only the preceding 756 closes for resampling. |
| ERR-005 | 2026-09-22 | Phase 2 | Temporary canary workflow runs overlapped, causing one derived-output git push to lose a race even though calculation and artifact upload succeeded. | Switched the permanent Phase 2 workflow to manual-only with concurrency control and removed the temporary canary trigger after baseline success. |
