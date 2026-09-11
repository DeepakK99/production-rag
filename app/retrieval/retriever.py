from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Chunk
from app.retrieval.models import RetrievalResult


def search_similar_chunks(
    session: Session,
    query_embedding: list[float],
    limit: int = 5,
) -> list[RetrievalResult]:
    distance = Chunk.embedding.cosine_distance(query_embedding)

    statement = (
        select(
            Chunk,
            distance.label("distance"),
        )
        .order_by(distance)
        .limit(limit)
    )

    rows = session.execute(statement).all()

    return [
        RetrievalResult(
            chunk=chunk,
            distance=distance,
        )
        for chunk, distance in rows
    ]
