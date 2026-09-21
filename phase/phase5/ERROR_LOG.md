# Phase 5 Error Log

| ID | Event | Action |
|---|---|---|
| P5-001 | Manuscript generation branch was opened before Phase 4 outputs were committed. | Phase 5 workflow will regenerate the Phase 3/4 derived outputs reproducibly before building the manuscript. |
| P5-002 | 2026-09-22 | Phase 5 | Adding SENSEX_index.parquet exposed a parser bug that attempted to treat index parquet filenames as option expiry dates. | Changed the shared baseline loop to skip all *_index.parquet files; affected phase branches were patched. |
