from dataclasses import dataclass

from app.retrieval.models import RetrievalResult


@dataclass
class Citation:
    source_id: int
    recipe_number: str | None
    recipe_name: str | None
    section: str | None
    pages: list[int]


def build_citations(results: list[RetrievalResult]) -> list[Citation]:
    citations = []

    for result in results:
        metadata = result.chunk.metadata_

        citations.append(
            Citation(
                source_id=result.chunk.id,
                recipe_number=metadata.get("recipe_number"),
                recipe_name=metadata.get("recipe_name"),
                section=metadata.get("section"),
                pages=metadata.get("pages", []),
            )
        )

    return citations
