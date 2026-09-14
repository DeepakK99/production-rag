from app.models import Chunk
from app.retrieval.citations import build_citations
from app.retrieval.models import RetrievalResult


def test_build_citations():
    chunk = Chunk(
        id=42,
        content="1. Clean and grate the carrots.",
        chunk_index=0,
        metadata_={
            "recipe_number": "12.8",
            "recipe_name": "Carrot Halva",
            "chapter_number": 12,
            "chapter_title": "DESSERTS AND OTHER GOODIES",
            "section": "Method",
            "pages": [77, 78],
        },
    )

    result = RetrievalResult(
        chunk=chunk,
        score=0.2,
        source="vector",
    )

    citations = build_citations([result])

    assert len(citations) == 1

    citation = citations[0]

    assert citation.source_id == 42
    assert citation.recipe_number == "12.8"
    assert citation.recipe_name == "Carrot Halva"
    assert citation.section == "Method"
    assert citation.pages == [77, 78]
