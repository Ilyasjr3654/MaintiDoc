from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "data" / "raw" / "pdf" / "bmw_i3"

pdfs = sorted(PDF_DIR.glob("*.pdf"))
print(f"Nombre de PDF : {len(pdfs)}")
for pdf in pdfs:
    with fitz.open(pdf) as doc:
        print(f"{pdf.name:45s} | {len(doc):2d} pages")
