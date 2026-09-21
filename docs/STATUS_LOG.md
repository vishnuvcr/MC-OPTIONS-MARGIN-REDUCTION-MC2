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
| 2.1 | Baseline reconstruction | DONE PROVISIONALLY | End-to-end data acquisition and corrected 5,000-path baseline run succeeded. |
| 2.2 | Baseline reconstruction | DONE PROVISIONALLY | 99 expiry rows evaluated; 98 valid, 1 skipped for no post-09:30 executable observation. |
| 2.3 | Baseline reconstruction | DONE PROVISIONALLY | 53 trades passed gross MC-EV > 0; corrected conditional realized win rate 77.36%; mean net P&L ₹1,702.98/trade. |
| 2.4 | Baseline reconstruction | DONE PROVISIONALLY | Sensex D3/rolling regime fields added to the baseline ledger. |
| 3.1 | Strike alteration search | DONE PROVISIONALLY | 53 finite strike configurations evaluated under identical provisional MC/cost/execution assumptions. |
| 3.2 | Strike alteration search | DONE PROVISIONALLY | Sensex fields carried into every candidate-expiry row for later stratification; not used as a candidate-ranking input. |
| 4.0 | Walk-forward robustness | IN PROGRESS | Building chronological holdouts, paired inference, stress testing and Sensex-regime stratification. |
