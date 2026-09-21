from __future__ import annotations

import json
from pathlib import Path

import requests

DATASET = "thetrademarkk/india-index-options-1m"
BASE = "https://huggingface.co"


def download(url: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.stat().st_size > 0:
        return
    with requests.get(url, stream=True, timeout=120, allow_redirects=True) as r:
        r.raise_for_status()
        with path.open("wb") as fh:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    fh.write(chunk)


def main() -> None:
    raw = Path("data/raw")
    raw.mkdir(parents=True, exist_ok=True)

    index_url = f"{BASE}/datasets/{DATASET}/resolve/main/index/NIFTY.parquet?download=true"
    download(index_url, raw / "NIFTY_index.parquet")

    api = f"{BASE}/api/datasets/{DATASET}/tree/main/options/NIFTY"
    params = {"recursive": "false", "expand": "false", "limit": "1000"}
    r = requests.get(api, params=params, timeout=120)
    r.raise_for_status()
    rows = r.json()

    files = sorted(
        x["path"] for x in rows
        if x.get("type") == "file" and x["path"].endswith(".parquet")
    )

    manifest = {"dataset": DATASET, "files": files, "count": len(files)}
    Path("data/raw/source_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    for rel in files:
        out = raw / Path(rel).name
        url = f"{BASE}/datasets/{DATASET}/resolve/main/{rel}?download=true"
        download(url, out)

    print(f"Downloaded/available option expiry files: {len(files)}")


if __name__ == "__main__":
    main()
