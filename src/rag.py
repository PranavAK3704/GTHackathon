from pathlib import Path
from typing import List


class RAGIndex:
    """
    Minimal stub for a RAG index.
    Can later be extended to use sentence-transformers + FAISS.
    """

    def __init__(self, docs_path: str):
        self.docs_path = Path(docs_path)
        self.chunks: List[str] = []

    def build(self) -> None:
        """
        For now, just load any .txt files in docs/ into a list of chunks.
        """
        self.chunks = []
        for p in self.docs_path.glob("*.txt"):
            self.chunks.append(p.read_text(encoding="utf-8"))

    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        """
        Very naive retrieval: just return first top_k chunks.
        (Good enough to show architecture for the assignment.)
        """
        return self.chunks[:top_k]
