from collections import defaultdict

from sqlalchemy.orm import Session

from app.retrieval.models import RetrievalResult

from .keyword_retriever import search_keyword_chunks
from .retriever import search_similar_chunks


def reciprocal_rank_fusion(
    result_lists: list[list[RetrievalResult]],
    k: int = 60,
) -> list[RetrievalResult]:
    scores = defaultdict(float)
    results_by_chunk_id = {}

    for results in result_lists:
        for rank, result in enumerate(results, start=1):
            chunk_id = result.chunk.id

            scores[chunk_id] += 1 / (k + rank)
            results_by_chunk_id[chunk_id] = result

    ranked_chunk_ids = sorted(
        scores,
        key=scores.get,
        reverse=True,
    )

    return [
        RetrievalResult(
            chunk=results_by_chunk_id[chunk_id].chunk,
            score=scores[chunk_id],
            source="hybrid",
        )
        for chunk_id in ranked_chunk_ids
    ]


def search_hybrid_chunks(
    session: Session,
    query: str,
    query_embedding: list[float],
    limit: int = 5,
) -> list[RetrievalResult]:
    vector_results = search_similar_chunks(
        session=session,
        query_embedding=query_embedding,
        limit=limit,
    )

    keyword_results = search_keyword_chunks(
        session=session,
        query=query,
        limit=limit,
    )

    return reciprocal_rank_fusion(
        [
            vector_results,
            keyword_results,
        ]
    )[:limit]
