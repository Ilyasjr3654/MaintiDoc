from __future__ import annotations

import hashlib
import io
from pathlib import Path
from typing import Any

import fitz  # PyMuPDF
from PIL import Image

from .chunking import chunk_text, clean_text


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def extract_pdf(
    pdf_path: Path,
    *,
    document_id: str,
    metadata: dict[str, Any],
    images_root: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    doc = fitz.open(pdf_path)
    document_images_dir = images_root / document_id
    document_images_dir.mkdir(parents=True, exist_ok=True)

    chunks: list[dict[str, Any]] = []
    visuals: list[dict[str, Any]] = []
    image_hash_to_path: dict[str, str] = {}

    for page_index, page in enumerate(doc):
        page_number = page_index + 1
        page_text = clean_text(page.get_text("text"))
        page_chunks = chunk_text(page_text)
        for chunk_index, chunk in enumerate(page_chunks, start=1):
            chunks.append(
                {
                    "chunk_id": f"{document_id}_P{page_number:02d}_C{chunk_index:02d}",
                    "document_id": document_id,
                    "filename": pdf_path.name,
                    "title": metadata["title"],
                    "manufacturer": "BMW",
                    "model": "i3",
                    "platform": "I01",
                    "system": metadata["system"],
                    "subsystem": metadata["subsystem"],
                    "problem": metadata["problem"],
                    "dtc_codes": metadata["dtc_codes"],
                    "page": page_number,
                    "element_type": "text",
                    "text": chunk.text,
                    "text_fingerprint": chunk.fingerprint,
                    "source_name": metadata["source_name"],
                    "source_url": metadata["source_url"],
                    "allowed_groups": ["technician", "maintenance_manager"],
                }
            )

        for image_index, image_info in enumerate(page.get_images(full=True), start=1):
            xref = image_info[0]
            try:
                extracted = doc.extract_image(xref)
            except Exception:
                continue
            image_bytes = extracted.get("image", b"")
            if not image_bytes:
                continue
            digest = sha256_bytes(image_bytes)
            width = int(extracted.get("width", 0) or 0)
            height = int(extracted.get("height", 0) or 0)
            # Écarte logos/icônes minuscules qui n'aident pas le VLM.
            if width < 120 or height < 90:
                continue

            duplicate_of = image_hash_to_path.get(digest)
            if duplicate_of:
                image_rel = duplicate_of
            else:
                ext = extracted.get("ext", "png")
                image_name = f"p{page_number:02d}_img{image_index:02d}_{digest[:10]}.{ext}"
                image_path = document_images_dir / image_name
                image_path.write_bytes(image_bytes)
                image_rel = image_path.relative_to(images_root.parent.parent).as_posix()
                image_hash_to_path[digest] = image_rel

            # Vérifie que l'image est lisible.
            try:
                with Image.open(io.BytesIO(image_bytes)) as pil_img:
                    mode = pil_img.mode
            except Exception:
                mode = "unknown"

            visuals.append(
                {
                    "image_id": f"{document_id}_P{page_number:02d}_I{image_index:02d}",
                    "document_id": document_id,
                    "filename": pdf_path.name,
                    "page": page_number,
                    "system": metadata["system"],
                    "subsystem": metadata["subsystem"],
                    "problem": metadata["problem"],
                    "dtc_codes": metadata["dtc_codes"],
                    "element_type": "image",
                    "image_path": image_rel,
                    "width": width,
                    "height": height,
                    "mode": mode,
                    "sha256": digest,
                    "duplicate_of": duplicate_of,
                    "source_name": metadata["source_name"],
                    "source_url": metadata["source_url"],
                    "allowed_groups": ["technician", "maintenance_manager"],
                }
            )

    doc_summary = {
        "document_id": document_id,
        "filename": pdf_path.name,
        "title": metadata["title"],
        "pages": len(doc),
        "system": metadata["system"],
        "subsystem": metadata["subsystem"],
        "problem": metadata["problem"],
        "dtc_codes": metadata["dtc_codes"],
        "source_name": metadata["source_name"],
        "source_url": metadata["source_url"],
        "pdf_sha256": sha256_file(pdf_path),
        "text_chunk_count": len(chunks),
        "visual_element_count": len(visuals),
    }
    doc.close()
    return chunks, visuals, doc_summary
