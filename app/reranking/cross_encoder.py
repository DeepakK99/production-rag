from sentence_transformers import CrossEncoder

from app.retrieval.models import RetrievalResult


class CrossEncoderReranker:
    def __init__(self, model: str):
        self.model = CrossEncoder(model)

    def rerank(
        self,
        query: str,
        results: list[RetrievalResult],
    ) -> list[RetrievalResult]:
        if not results:
            return []

        pairs = [
            (query, result.chunk.content)
            for result in results
        ]

        scores = self.model.predict(pairs)

        reranked = [
            (result, float(score))
            for result, score in zip(
                results,
                scores,
                strict=True,
            )
        ]

        reranked.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        return [
            RetrievalResult(
                chunk=result.chunk,
                score=score,
                source="reranker",
            )
            for result, score in reranked
        ]