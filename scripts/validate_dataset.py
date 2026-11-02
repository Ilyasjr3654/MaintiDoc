from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from maintidoc_dataset.config import get_settings
from maintidoc_dataset.io_utils import read_jsonl


def main() -> None:
    s = get_settings(ROOT)
    problems: list[str] = []

    pdfs = sorted(s.pdf_dir.glob("*.pdf"))
    if len(pdfs) != 35:
        problems.append(f"35 PDF attendus, trouvé {len(pdfs)}")

    with s.documents_csv.open("r", encoding="utf-8", newline="") as handle:
        documents = list(csv.DictReader(handle))
    chunks = read_jsonl(s.text_chunks_jsonl)
    visuals = read_jsonl(s.visual_elements_jsonl)
    train = read_jsonl(s.reranker_train_jsonl)
    val = read_jsonl(s.reranker_validation_jsonl)
    test = read_jsonl(s.reranker_test_jsonl)
    eval_cases = read_jsonl(s.eval_cases_jsonl)

    if len(documents) != 35:
        problems.append(f"documents.csv: 35 lignes attendues, trouvé {len(documents)}")
    if len(chunks) < 70:
        problems.append(f"Trop peu de chunks texte: {len(chunks)}")
    if len(visuals) < 35:
        problems.append(f"Trop peu d'éléments visuels: {len(visuals)}")
    if len(eval_cases) < 70:
        problems.append(f"Trop peu de cas d'évaluation: {len(eval_cases)}")

    document_ids = [d["document_id"] for d in documents]
    duplicates = [k for k, v in Counter(document_ids).items() if v > 1]
    if duplicates:
        problems.append(f"document_id dupliqués: {duplicates}")

    split_docs = {
        "train": {x["document_id"] for x in train},
        "validation": {x["document_id"] for x in val},
        "test": {x["document_id"] for x in test},
    }
    if split_docs["train"] & split_docs["validation"]:
        problems.append("Fuite de documents train -> validation")
    if split_docs["train"] & split_docs["test"]:
        problems.append("Fuite de documents train -> test")
    if split_docs["validation"] & split_docs["test"]:
        problems.append("Fuite de documents validation -> test")

    print("=== Validation dataset MaintiDoc ===")
    print(f"PDF                  : {len(pdfs)}")
    print(f"Documents            : {len(documents)}")
    print(f"Chunks texte         : {len(chunks)}")
    print(f"Éléments visuels     : {len(visuals)}")
    print(f"Reranker train       : {len(train)}")
    print(f"Reranker validation  : {len(val)}")
    print(f"Reranker test        : {len(test)}")
    print(f"Cas évaluation       : {len(eval_cases)}")

    if problems:
        print("\nÉCHEC:")
        for p in problems:
            print(" -", p)
        raise SystemExit(1)
    print("\nOK - dataset cohérent.")


if __name__ == "__main__":
    main()
