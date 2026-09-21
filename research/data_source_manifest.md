# Data Source Manifest

## Official exchange sources

- NSE historical derivatives reports: https://www.nseindia.com/all-reports-derivatives
- NSE historical reports catalogue: https://www.nseindia.com/static/resources/historical-reports-capital-market-daily-monthly-archives
- NSE SPAN risk parameter files: https://www.nseindia.com/static/products-services/equity-derivatives-span-risk-parameter-files

## Open historical data sources

- NSE-FNO-Data-bank: https://github.com/SantoshSrinivas79/NSE-FNO-Data-bank
- Hugging Face rissin/nse-options-intraday: https://huggingface.co/datasets/rissin/nse-options-intraday
- Hugging Face thetrademarkk/india-index-options-1m: https://huggingface.co/datasets/thetrademarkk/india-index-options-1m

## Open-source implementations

- nse-options-data-collector: https://github.com/BarathGB007/nse-options-data-collector
- Indian-market-data-pipeline: https://github.com/JATINDHURVE/Indian-market-data-pipeline
- bhav: https://github.com/rajmaurya0904/bhav

## Data hierarchy

1. NSE/NSE Clearing official files.
2. Broker historical contract data with explicit provenance.
3. Open datasets, after schema and spot checks.
4. Secondary websites for cross-checking only.

## Critical data distinction

Daily bhavcopy/settlement data can validate expiry outcomes and contract metadata. The 09:30 execution rule requires intraday option observations. Intraday data therefore has to be tracked as a separate coverage requirement.

## Caching policy

The repository will cache the derived 756-session research dataset, source manifests and checksums. Large or restricted raw datasets will not be copied wholesale into the repository.
