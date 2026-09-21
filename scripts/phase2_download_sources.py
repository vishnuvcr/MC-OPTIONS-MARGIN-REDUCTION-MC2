from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path

import requests

DATASET = "thetrademarkk/india-index-options-1m"
BASE = "https://huggingface.co"

# July 2024 leaves a safety buffer for the first eligible D3 after a full
# 756-session history can be assembled from the dataset's May-2021 start.
MIN_EXPIRY = date(2024, 7, 1)
MAX_WORKERS = 6


def download(url: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.stat().st_size > 0:
        return

    with requests.get(url, stream=True, timeout=300, allow_redirects=True) as r:
        r.raise_for_status()
        with path.open("wb") as fh:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    fh.write(chunk)


def relevant_expiry(rel: str) -> bool:
    try:
        expiry = date.fromisoformat(Path(rel).stem)
    except ValueError:
        return False
    return expiry >= MIN_EXPIRY


def main() -> None:
    raw = Path("data/raw")
    raw.mkdir(parents=True, exist_ok=True)

    for symbol in ("NIFTY", "SENSEX"):
        index_url = f"{BASE}/datasets/{DATASET}/resolve/main/index/{symbol}.parquet?download=true"
        download(index_url, raw / f"{symbol}_index.parquet")

    api = f"{BASE}/api/datasets/{DATASET}/tree/main/options/NIFTY"
    params = {"recursive": "false", "expand": "false", "limit": "1000"}
    r = requests.get(api, params=params, timeout=120)
    r.raise_for_status()
    rows = r.json()

    files = sorted(
        x["path"] for x in rows
        if x.get("type") == "file"
        and x["path"].endswith(".parquet")
        and relevant_expiry(x["path"])
    )

    manifest = {
        "dataset": DATASET,
        "min_expiry": MIN_EXPIRY.isoformat(),
        "files": files,
        "count": len(files),
    }
    Path("data/raw/source_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    futures = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        for rel in files:
            out = raw / Path(rel).name
            url = f"{BASE}/datasets/{DATASET}/resolve/main/{rel}?download=true"
            futures[pool.submit(download, url, out)] = rel

        completed = 0
        for future in as_completed(futures):
            rel = futures[future]
            future.result()
            completed += 1
            print(f"[{completed}/{len(files)}] {rel}")

    print(f"Downloaded/available option expiry files: {len(files)}")


if __name__ == "__main__":
    main()
