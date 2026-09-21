# Manuscript Data Dictionary

| Field | Definition |
|---|---|
| expiry | NIFTY option expiry date |
| d3 | Third trading session before expiry |
| spot_0930 | First executable NIFTY spot observation strictly after 09:30 IST |
| sensex_0930 | First executable Sensex spot observation strictly after 09:30 IST |
| sensex_prev_close | Previous Sensex trading-session close before D3 |
| sensex_d3_gap_pct | Sensex 09:30 level / previous close - 1 |
| nifty_d3_gap_pct | NIFTY 09:30 level / previous close - 1 |
| sensex_prior20d_log_return | Log return over prior 20 Sensex sessions |
| nifty_prior20d_log_return | Log return over prior 20 NIFTY sessions |
| nifty_minus_sensex_prior20d_log_return | Relative prior-20-session NIFTY return minus Sensex return |
| gross_mc_ev_points | Mean simulated gross terminal strategy EV before explicit transaction costs |
| gate | gross_mc_ev > 0 |
| realized_net_pnl_inr | Expiry-settled realised P&L including slippage, brokerage and STT |
| win | realised net P&L > 0 |
| es95_inr_proxy | Expected-shortfall proxy from simulated net-P&L distribution |
| es99_inr_proxy | Expected-shortfall proxy from simulated net-P&L distribution |
| shock9p3_gross_loss_inr | Gross expiry loss proxy under ±9.3% spot stress |
