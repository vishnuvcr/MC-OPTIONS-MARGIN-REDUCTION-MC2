# Phase 2 Error Log

| ID | Event | Action |
|---|---|---|
| P2-001 | First GitHub Actions run is acquiring the source dataset; live log blob is not available while the step is in progress. | Track status via workflow/job API and do not infer a result from absent logs. |
| P2-002 | Baseline engine was patched after the initial workflow commit to fix result aggregation when no skipped rows are present and to clamp ES proxy to non-negative values. | The next workflow run will use the corrected code. |
| P2-003 | Phase 2 | Previous successful canary showed 99 eligible expiries but all were incorrectly skipped because the expiry lookup used a pre-D3 history slice. | Fixed bootstrap calendar lookup to use the full trading calendar while retaining only the prior 756 closes for resampling. Also enforced strict post-09:30 executable timestamps and positive volume for option entry. |
