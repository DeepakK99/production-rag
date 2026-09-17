from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Chunk
from app.retrieval.models import RetrievalResult


def search_similar_chunks(
    session: Session,
    query_embedding: list[float],
    limit: int = 50, # increasing size from 5 to 50
) -> list[RetrievalResult]:
    distance = Chunk.embedding.cosine_distance(query_embedding)

    statement = (
        select(
            Chunk,
            distance.label("distance"),
        )
        .where(Chunk.embedding.is_not(None))
        .order_by(distance)
        .limit(limit)
    )

    rows = session.execute(statement).all()

    return [
        RetrievalResult(
            chunk=chunk,
            score=1.0 - float(distance),
            source="vector",
        )
        for chunk, distance in rows
    ]
