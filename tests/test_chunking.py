import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from maintidoc_dataset.chunking import chunk_text, clean_text


def test_clean_text():
    assert clean_text("Bonjour   BMW\n\n\nTest") == "Bonjour BMW\n\nTest"


def test_chunk_text_returns_chunks():
    text = ("BMW i3 défaut d'isolation haute tension. " * 40) + "\n\n" + ("ISTA diagnostic. " * 40)
    chunks = chunk_text(text, min_chars=100, target_chars=300, max_chars=500)
    assert len(chunks) >= 2
    assert all(c.text for c in chunks)
