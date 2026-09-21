# Combined Data Dictionary

| Field | Definition |
|---|---|
| expiry | NIFTY option expiry date |
| d3 | Third trading session before expiry |
| spot_0930 | First executable NIFTY spot observation strictly after 09:30 IST |
| sensex_0930 | First executable Sensex observation strictly after 09:30 IST |
| target_q20 / target_q35 / target_q65 / target_q80 | Requested terminal MC quantiles |
| mapped_P20 / mapped_P35 / mapped_P65 / mapped_P80 | Distinct listed strikes selected from target quantiles |
| gross_mc_ev_points | Mean simulated gross terminal strategy EV |
| gate | gross MC-EV > 0 |
| realized_net_pnl_inr | Expiry-settled net P&L including locked slippage, brokerage and STT |
| es95_inr_proxy | Expected shortfall risk-capital proxy |
| es99_inr_proxy | Expected shortfall risk-capital proxy |
| shock9p3_gross_loss_inr | Gross loss under the registered ±9.3% spot-shock diagnostic |
| capital_proxy | Gated mean shock9p3 gross-loss proxy used in the new capital track |
| entry_capital | Actual funds needed to open the position when exchange/broker margin is directly reconstructed |
| peak_capital | Maximum required capital while position is open |
| span | Historical portfolio SPAN requirement |
| exposure | Exposure / ELM margin |
| additional | Additional applicable margin, including expiry-day components where the file supports it |
