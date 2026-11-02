from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from maintidoc_dataset.config import get_settings
from maintidoc_dataset.io_utils import read_jsonl

s = get_settings(ROOT)
chunks = read_jsonl(s.text_chunks_jsonl)
visuals = read_jsonl(s.visual_elements_jsonl)

print("=== Exemple de chunk ===")
print(json.dumps(chunks[0], ensure_ascii=False, indent=2) if chunks else "Aucun chunk")
print("\n=== Exemple visuel ===")
print(json.dumps(visuals[0], ensure_ascii=False, indent=2) if visuals else "Aucun visuel")
