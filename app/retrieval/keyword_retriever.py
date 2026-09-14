from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Chunk
from app.retrieval.models import RetrievalResult


def search_keyword_chunks(
    session: Session,
    query: str,
    limit: int = 5,
) -> list[RetrievalResult]:
    search_query = func.websearch_to_tsquery(
        "english",
        query,
    )

    rank = func.ts_rank_cd(
        Chunk.search_vector,
        search_query,
    )

    statement = (
        select(
            Chunk,
            rank.label("rank"),
        )
        .where(Chunk.search_vector.op("@@")(search_query))
        .order_by(rank.desc())
        .limit(limit)
    )

    rows = session.execute(statement).all()

    return [
        RetrievalResult(
            chunk=chunk,
            score=float(rank),
            source="keyword",
        )
        for chunk, rank in rows
    ]
