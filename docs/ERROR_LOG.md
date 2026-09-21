# Error Log

| ID | Date | Phase | Error / limitation | Action |
|---|---|---|---|---|
| ERR-001 | 2026-09-22 | Foundation | Repository was empty; no prior files, plan, results or data were available. | Treat as clean initialization; do not invent prior history. |
| ERR-002 | 2026-09-22 | Foundation | Direct container network access to Hugging Face failed with DNS resolution error. | Do not claim local dataset download. Use web metadata and reproducible ingestion instructions instead. |
| ERR-003 | 2026-09-22 | Phase 1 | Some GitHub connector writes for code/workflow artifacts were rejected. | Keep accepted research artifacts authoritative and do not claim rejected files exist. |
| ERR-004 | 2026-09-22 | Phase 2 | First successful numerical canary revealed an expiry-calendar bug: expiry lookup was performed inside a pre-D3 history slice, causing valid expiries to be marked unavailable. | Corrected the bootstrap calendar lookup to use the full trading calendar while keeping only the preceding 756 closes for resampling. |
| ERR-005 | 2026-09-22 | Phase 2 | Temporary canary workflow runs overlapped, causing one derived-output git push to lose a race even though calculation and artifact upload succeeded. | Switched the permanent Phase 2 workflow to manual-only with concurrency control and removed the temporary canary trigger after baseline success. |
| ERR-006 | 2026-09-22 | Phase 2 | Realized P&L initially omitted the direct cash-flow impact of the locked 2-point entry slippage. | Corrected the implementation and reran the baseline; the earlier 81.13%/₹2,442 result is superseded by 77.36%/₹1,702.98. |
| ERR-007 | 2026-09-22 | Phase 3 | Sensex-aware candidate code initially ran with the older NIFTY-only source loader. | Added SENSEX.parquet acquisition to the branch loader and reran the candidate search. |
| ERR-008 | 2026-09-22 | Phase 3 | Requiring valid D3 Sensex information reduced usable expiries from 98 to 97. | Treat missing Sensex observations as data-quality exclusions; do not impute or forward-fill. |
| ERR-009 | 2026-09-22 | Phase 5 | Adding SENSEX_index.parquet exposed a parser bug that attempted to treat index parquet filenames as option expiry dates. | Changed the shared baseline loop to skip all *_index.parquet files; affected phase branches were patched. |

| ERR-010 | 2026-09-22 | Research direction | Prior response framed the next question around recovery of the Monte Carlo implementation rather than the user's primary objective of reducing total trading capital/margin by adjusting BATMAN parameters. | Corrected the research framing: parameter-driven actual capital/margin minimization is the primary objective; MC recovery remains a prerequisite for an authoritative rerun. |
