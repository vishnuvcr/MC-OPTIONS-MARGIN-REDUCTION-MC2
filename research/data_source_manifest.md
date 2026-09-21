# Data Source Manifest

## Primary intraday research source

**TradeMarkk — India Index & Options 1-minute OHLC**

- URL: https://huggingface.co/datasets/thetrademarkk/india-index-options-1m
- Schema: `timestamp`, `open`, `high`, `low`, `close`, `volume`, `open_interest`, `trading_day`, `symbol`.
- Spot index files: `index/NIFTY.parquet`, `index/SENSEX.parquet`.
- Option files: `options/{SYMBOL}/{EXPIRY}.parquet`.
- Timestamps are documented as IST.
- Coverage is described as approximately 2021–2026 and option coverage is partial for illiquid/far strikes.
- License: CC BY-NC 4.0; raw redistribution is therefore handled conservatively.

## Official cross-check sources

### BSE Sensex
- BSE market-data service: https://marketdata.bseindia.com/
- BSE Sensex page / historical values: https://www.bseindia.com/sensex/code/45
- BSE index archive referenced by BSE materials: https://www.bseindia.com/Indices/IndexArchiveData.html

### NSE/NIFTY
- NSE historical index data: https://www.niftyindices.com/reports/historical-data
- NSE derivatives reports: https://www.nseindia.com/all-reports-derivatives
- NSE FII/DII reports: https://www.nseindia.com/reports/fii-dii

## Sensex-specific use

Sensex is required in Phases 1–5 as a non-look-ahead diagnostic/cross-market regime series:
- D3 post-09:30 Sensex level;
- previous close;
- D3 opening gap;
- prior-20-session Sensex log return;
- NIFTY minus Sensex prior-20-session return.

Sensex information is never allowed to change the locked NIFTY BATMAN signal unless a separate cross-index ablation is explicitly registered.
