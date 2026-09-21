# Phase 2 — SPAN Cache / Manifest Specification

## Purpose
Keep important margin inputs reproducible and avoid downloading the same large SPAN files on every workflow run.

## Raw cache
Expected path: data/raw/span/

Files should use the exchange-provided naming convention, for example nsccl.YYYYMMDD.s.spn for end-of-day files. Begin-of-day/intraday files are stored with their exact source names.

## Manifest
File: data/raw/span/span_manifest.csv

Required columns:
- as_of_date
- file_name
- file_type (BOD / INTRADAY / EOD)
- source_url
- sha256
- downloaded_at_utc
- source_status

## Selection rule for entry capital
1. D3 BOD file if available.
2. Otherwise previous trading-day EOD file.
3. Otherwise mark margin as unavailable; do not substitute a current-date file.

## Selection rule for peak capital
Use every available dated SPAN observation between D3 and expiry that is attributable to the open position. Store the maximum calculated total.

## Cache policy
Raw exchange files should be cached only when redistribution is permitted. Otherwise retain checksums, source manifests, and compact derived NIFTY-only extracts sufficient for reproducibility.

## Derived cache
Where raw redistribution is restricted, cache a compact NIFTY-only derived dataset containing the contracts and risk arrays needed by the registered BATMAN parameter grid, plus file checksum and parser version.