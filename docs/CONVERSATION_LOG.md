# Conversation / Decision Record

## 2026-09-22

### User request
Research the possibility of altering NIFTY BATMAN spots/strikes to reduce margin while retaining profit and win rate. User supplied a locked final rule:
- D3 trading session before expiry
- 09:30 IST signal
- 756-session bootstrap Monte Carlo, 5,000 paths
- gross MC-EV gate > 0
- P20/P35/P65/P80 terminal quantiles mapped to nearest unique available strikes
- +1 P35 PE, -2 P20 PE, +1 P65 CE, -2 P80 CE
- first executable observation after 09:30
- expiry exit
- 2 option points slippage per execution leg
- brokerage + STT + historical lot size
- ES95/ES99 sizing proxy

### Research decision
The supplied rule is treated as the locked baseline/control. Candidate alterations will be evaluated against it with the same signal, execution, cost and sizing framework.

### Repository observation
The supplied GitHub repository was empty at the start of this work. No prior plan, results, data or logs were available.

### Data limitation observed
Direct container DNS/network access to Hugging Face was unavailable. No local raw dataset download is being claimed on that basis. Source metadata and reproducible ingestion instructions are being recorded instead.
