from pathlib import Path
import fitz


def test_35_pdfs_exist():
    root = Path(__file__).resolve().parents[1]
    pdfs = list((root / "data" / "raw" / "pdf" / "bmw_i3").glob("*.pdf"))
    assert len(pdfs) == 35


def test_pdfs_are_readable():
    root = Path(__file__).resolve().parents[1]
    for pdf in (root / "data" / "raw" / "pdf" / "bmw_i3").glob("*.pdf"):
        with fitz.open(pdf) as doc:
            assert len(doc) == 8
