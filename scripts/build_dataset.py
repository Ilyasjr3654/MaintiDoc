from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from maintidoc_dataset.config import get_settings
from maintidoc_dataset.pipeline import run_pipeline


def main() -> None:
    settings = get_settings(ROOT)
    stats = run_pipeline(settings)
    print("\n=== Dataset MaintiDoc généré ===")
    for key, value in stats.items():
        print(f"{key:24s}: {value}")


if __name__ == "__main__":
    main()
