from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass


SPACE_RE = re.compile(r"[ \t]+")
BLANK_RE = re.compile(r"\n\s*\n+")


@dataclass(frozen=True)
class Chunk:
    text: str
    fingerprint: str


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ").replace("\r", "\n")
    lines = []
    for line in text.splitlines():
        line = SPACE_RE.sub(" ", line).strip()
        if not line:
            lines.append("")
            continue
        # Supprime quelques artefacts de pagination/export sans enlever le contenu métier.
        if re.fullmatch(r"\d+", line):
            continue
        lines.append(line)
    cleaned = "\n".join(lines)
    cleaned = BLANK_RE.sub("\n\n", cleaned)
    return cleaned.strip()


def _paragraphs(text: str) -> list[str]:
    text = clean_text(text)
    if not text:
        return []
    paragraphs = [p.strip() for p in BLANK_RE.split(text) if p.strip()]
    if len(paragraphs) == 1:
        # Les exports Slides ont souvent une seule grande zone textuelle.
        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    return paragraphs


def _fingerprint(text: str) -> str:
    normalized = re.sub(r"\W+", "", text.lower(), flags=re.UNICODE)
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()


def chunk_text(
    text: str,
    *,
    min_chars: int = 240,
    target_chars: int = 900,
    max_chars: int = 1700,
    overlap_paragraphs: int = 1,
) -> list[Chunk]:
    paragraphs = _paragraphs(text)
    if not paragraphs:
        return []

    chunks: list[Chunk] = []
    current: list[str] = []
    current_len = 0

    def flush() -> None:
        nonlocal current, current_len
        if not current:
            return
        value = "\n".join(current).strip()
        if len(value) >= min_chars:
            chunks.append(Chunk(text=value, fingerprint=_fingerprint(value)))
        keep = current[-overlap_paragraphs:] if overlap_paragraphs else []
        current = list(keep)
        current_len = sum(len(p) for p in current)

    for paragraph in paragraphs:
        p_len = len(paragraph)
        projected = current_len + p_len + (1 if current else 0)
        if current and projected > max_chars:
            flush()
        current.append(paragraph)
        current_len += p_len + 1
        if current_len >= target_chars:
            flush()

    if current:
        value = "\n".join(current).strip()
        if len(value) >= min_chars and (not chunks or value != chunks[-1].text):
            chunks.append(Chunk(text=value, fingerprint=_fingerprint(value)))
        elif chunks and value and value != chunks[-1].text:
            # Rattache un petit reliquat à la fin du chunk précédent au lieu de créer un chunk titre/bruit.
            merged = chunks[-1].text + "\n" + value
            chunks[-1] = Chunk(text=merged, fingerprint=_fingerprint(merged))

    # Déduplication locale.
    unique: list[Chunk] = []
    seen: set[str] = set()
    for chunk in chunks:
        if chunk.fingerprint in seen:
            continue
        seen.add(chunk.fingerprint)
        unique.append(chunk)
    return unique
