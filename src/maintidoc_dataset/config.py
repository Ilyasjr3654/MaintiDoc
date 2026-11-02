from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    root: Path
    pdf_dir: Path
    original_sources_dir: Path
    images_dir: Path
    metadata_dir: Path
    processed_dir: Path
    reranker_dir: Path
    evaluation_dir: Path
    corpus_index_csv: Path
    documents_csv: Path
    text_chunks_jsonl: Path
    visual_elements_jsonl: Path
    document_index_jsonl: Path
    reranker_train_jsonl: Path
    reranker_validation_jsonl: Path
    reranker_test_jsonl: Path
    eval_cases_jsonl: Path


def get_settings(root: Path | None = None) -> Settings:
    root = (root or Path(__file__).resolve().parents[2]).resolve()
    data = root / "data"
    return Settings(
        root=root,
        pdf_dir=data / "raw" / "pdf" / "bmw_i3",
        original_sources_dir=data / "raw" / "pdf" / "original_sources",
        images_dir=data / "raw" / "images",
        metadata_dir=data / "metadata",
        processed_dir=data / "processed",
        reranker_dir=data / "reranker",
        evaluation_dir=data / "evaluation",
        corpus_index_csv=data / "metadata" / "corpus_index.csv",
        documents_csv=data / "metadata" / "documents.csv",
        text_chunks_jsonl=data / "processed" / "text_chunks.jsonl",
        visual_elements_jsonl=data / "processed" / "visual_elements.jsonl",
        document_index_jsonl=data / "processed" / "document_index.jsonl",
        reranker_train_jsonl=data / "reranker" / "train.jsonl",
        reranker_validation_jsonl=data / "reranker" / "validation.jsonl",
        reranker_test_jsonl=data / "reranker" / "test.jsonl",
        eval_cases_jsonl=data / "evaluation" / "eval_cases.jsonl",
    )


def ensure_directories(settings: Settings) -> None:
    for path in (
        settings.pdf_dir,
        settings.original_sources_dir,
        settings.images_dir,
        settings.metadata_dir,
        settings.processed_dir,
        settings.reranker_dir,
        settings.evaluation_dir,
    ):
        path.mkdir(parents=True, exist_ok=True)
