from sqlalchemy import tuple_
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from app.retrieval.models import RetrievalResult
from app.models import Chunk


def expand_recipes(
    session: Session,
    results: list[RetrievalResult],
) -> list[RetrievalResult]:
    recipe_scores = {}

    for result in results:
        key = (
            result.chunk.document_id,
            result.chunk.metadata_.get("recipe_number"),
        )

        recipe_scores[key] = max(
            recipe_scores.get(key, float("-inf")),
            result.score,
        )
    
    target_pairs = set()

    for result in results:
        doc_id = result.chunk.document_id
        recipe_num = result.chunk.metadata_.get("recipe_number")
        
        if doc_id is not None and recipe_num is not None:
            target_pairs.add((doc_id, str(recipe_num)))

    if not target_pairs:
        return []

    stmt = (
        select(Chunk)
        .where(
            tuple_(
                Chunk.document_id,
                Chunk.metadata_['recipe_number'].as_string()
            ).in_(list(target_pairs))
        )
    )

    chunks = session.scalars(stmt).all()
    chunks.sort(key=lambda chunk: chunk.chunk_index)

    expanded_results = []

    for chunk in chunks:
        key = (
            chunk.document_id,
            chunk.metadata_.get("recipe_number"),
        )

        expanded_results.append(
            RetrievalResult(
                chunk=chunk,
                score=recipe_scores[key],
                source="recipe_expansion",
            )
        )

    return expanded_results
    