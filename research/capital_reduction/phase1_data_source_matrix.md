# Phase 1 — Data Source Matrix

| Data requirement | Preferred source | Secondary source | Intended use | Status |
|---|---|---|---|---|
| Historical NSE SPAN risk arrays / parameters | NSE / NSE Clearing historical F&O reports | Open-source mirrors only for cross-check | Reconstruct portfolio margin by date | AVAILABLE SOURCE FAMILY |
| NSE F&O market reports | NSE historical F&O reports / UDiFF | Existing MC2 intraday dataset | Settlement, OI, volume, participant and contract cross-checks | AVAILABLE |
| NIFTY 1-minute spot | Existing MC2 TradeMarkk source | Other validated intraday providers | D3 spot and execution alignment | AVAILABLE |
| NIFTY 1-minute options | Existing MC2 TradeMarkk source | rissin/nse-options-intraday | Four-leg entry prices, OI, volume, liquidity | AVAILABLE WITH COVERAGE LIMITS |
| SENSEX 1-minute spot | BSE official data | Existing MC2 TradeMarkk source | Cross-market diagnostic retained from prior track | AVAILABLE |
| India VIX | NSE historical India VIX archive | Derived realised-volatility measures | Regime stratification | AVAILABLE |
| FII/FPI/DII data | NSE reports | Other exchange/public datasets | Market-regime diagnostics | AVAILABLE |
| Historical lot sizes | NSE contract specifications / historical circulars | Validated public mirrors | Convert per-point P&L and margin to rupees | AVAILABLE |
| Transaction costs | SEBI/NSE historical rules plus project cost schedule | Broker documentation | Net P&L | AVAILABLE / DATE-SPECIFIC VALIDATION REQUIRED |
| Paytm Money margin | Paytm Money margin calculator / attributable observations | Paytm Money historical documentation | Broker-level total entry capital | PARTIALLY OBSERVABLE |

## Source notes

NSE's current derivatives report hub lists historical SPAN files, F&O bhavcopy/UDiFF data, daily volatility, settlements, participant-wise open interest and trading volumes, FII derivatives statistics and other derivative reports. 

NSE Clearing's SPAN documentation states that portfolio risk is evaluated using standardized price and volatility scenarios and that risk-parameter files are supplied to members for margin calculation.

Paytm Money states that initial margin for overnight F&O positions consists of SPAN + exposure margin, that option-writing margin is exchange-defined, and that combined hedge positions can reduce overall margin.

The TradeMarkk public dataset provides 1-minute NIFTY/BANKNIFTY/SENSEX index and option data in Parquet with IST timestamps, but its own documentation warns that illiquid/far-strike option coverage is partial; it therefore remains a reproducibility source rather than the unquestioned canonical exchange record.

BSE's market-data service provides exchange-verified indices OHLC feeds including Sensex. The BSE Sensex page also exposes previous close, open, high, low and a historical-values entry point.

## URLs
- NSE F&O reports: https://www.nseindia.com/all-reports-derivatives
- NSE equity derivative market reports: https://www.nseindia.com/static/regulations/segment-wise-historical-reports-equity-derivatives-market
- NSE historical reports: https://www.nseindia.com/static/resources/historical-reports-capital-market-daily-monthly-archives
- NSE Clearing SPAN risk parameters: https://www.nseclearing.in/risk-management/equity-derivatives/span-risk-parameters
- NSE SPAN parameter documentation: https://www.nseindia.com/static/products-services/equity-derivatives-span-risk-parameter-files
- Paytm Money margin FAQ: https://www.paytmmoney.com/stocks/customer/fno-faq/margin-leverage/margin/what-is-margin-call-requirement-received-notification-email-from-paytm-money
- Paytm Money margin calculator: https://www.paytmmoney.com/blog/margin-calculator/
- TradeMarkk data: https://huggingface.co/datasets/thetrademarkk/india-index-options-1m
- BSE market data: https://marketdata.bseindia.com/
- BSE Sensex page: https://www.bseindia.com/sensex/code/45