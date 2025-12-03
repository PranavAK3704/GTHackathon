from __future__ import annotations

import logging
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)

try:
    from sentence_transformers import SentenceTransformer
    import faiss
except ImportError:  # RAG will gracefully degrade if libs missing
    SentenceTransformer = None
    faiss = None

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


class RAGIndex:
    """
    Simple RAG index that loads .txt and .pdf documents from a folder,
    chunks them, builds embeddings, and performs similarity search.
    """

    def __init__(self, docs_path: str):
        self.docs_path = Path(docs_path)
        self.model: SentenceTransformer | None = None
        self.index: faiss.IndexFlatL2 | None = None  # type: ignore[type-arg]
        self.chunks: List[str] = []

    def _load_documents(self) -> List[str]:
        texts: List[str] = []

        if not self.docs_path.exists():
            logger.warning("RAG docs path %s does not exist", self.docs_path)
            return texts

        for path in self.docs_path.glob("**/*"):
            if path.suffix.lower() == ".txt":
                try:
                    texts.append(path.read_text(encoding="utf-8", errors="ignore"))
                except Exception as exc:
                    logger.warning("Failed to read %s: %s", path, exc)
            elif path.suffix.lower() == ".pdf" and PdfReader is not None:
                try:
                    reader = PdfReader(str(path))
                    pages = [page.extract_text() or "" for page in reader.pages]
                    texts.append("\n".join(pages))
                except Exception as exc:
                    logger.warning("Failed to read PDF %s: %s", path, exc)

        return texts

    @staticmethod
    def _chunk_text(text: str, chunk_size: int = 600, overlap: int = 120) -> List[str]:
        """
        Very simple character-based chunking. Enough for small docs.
        """
        chunks: List[str] = []
        start = 0
        length = len(text)

        if length == 0:
            return chunks

        while start < length:
            end = min(start + chunk_size, length)
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start += chunk_size - overlap

        return chunks

    def build(self) -> None:
        """
        Build the FAISS index. Call once at startup.
        """
        if SentenceTransformer is None or faiss is None:
            logger.warning(
                "sentence-transformers or faiss-cpu not installed. RAG will be disabled."
            )
            return

        raw_texts = self._load_documents()
        for text in raw_texts:
            self.chunks.extend(self._chunk_text(text))

        if not self.chunks:
            logger.warning("No chunks built for RAG from %s", self.docs_path)
            return

        logger.info("Building RAG index over %d chunks", len(self.chunks))

        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = self.model.encode(self.chunks)
        dim = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

        logger.info("RAG index built with dimension %d", dim)

    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        """
        Retrieve top_k similar chunks for the given query.
        """
        if not self.chunks or self.index is None or self.model is None:
            return []

        q_emb = self.model.encode([query])
        distances, indices = self.index.search(q_emb, top_k)

        results: List[str] = []
        for i in indices[0]:
            if 0 <= i < len(self.chunks):
                results.append(self.chunks[i])

        return results
