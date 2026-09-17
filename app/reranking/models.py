from typing import Protocol

from app.retrieval.models import RetrievalResult


class Reranker(Protocol):
    def rerank(
        self,
        query: str,
        results: list[RetrievalResult],
    ) -> list[RetrievalResult]:
        ...