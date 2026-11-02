from __future__ import annotations

import csv
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import requests

from maintidoc_dataset.config import get_settings


def safe_name(url: str, fallback: str) -> str:
    name = Path(urlparse(url).path).name or fallback
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name)
    return name if name.lower().endswith(".pdf") else name + ".pdf"


def main() -> None:
    s = get_settings(ROOT)
    s.original_sources_dir.mkdir(parents=True, exist_ok=True)

    with s.corpus_index_csv.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    seen: set[str] = set()
    ok = 0
    failed = 0
    for row in rows:
        url = row["url_source"].strip()
        if not url or url in seen:
            continue
        seen.add(url)
        target = s.original_sources_dir / safe_name(url, f"source_{row['numero']}")
        if target.exists() and target.stat().st_size > 1000:
            print(f"SKIP {target.name}")
            ok += 1
            continue
        try:
            response = requests.get(url, timeout=30, headers={"User-Agent": "MaintiDocDataset/0.1"})
            response.raise_for_status()
            data = response.content
            if not data.startswith(b"%PDF"):
                raise ValueError("La réponse n'est pas un PDF")
            target.write_bytes(data)
            print(f"OK   {target.name} ({len(data) // 1024} KiB)")
            ok += 1
        except Exception as exc:
            print(f"FAIL {url} -> {exc}")
            failed += 1

    print(f"\nSources uniques : {len(seen)} | téléchargées/existantes : {ok} | échecs : {failed}")
    if failed:
        print("Les échecs réseau n'empêchent pas la construction du dataset curaté.")


if __name__ == "__main__":
    main()
