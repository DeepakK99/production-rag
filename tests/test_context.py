from app.models import Chunk
from app.retrieval.context import build_context
from app.retrieval.models import RetrievalResult


def test_build_context():
    chunk = Chunk(
        content="1. Clean and grate the carrots.",
        chunk_index=0,
        metadata_={
            "recipe_number": "12.8",
            "recipe_name": "Carrot Halva",
            "chapter_number": 12,
            "chapter_title": "DESSERTS AND OTHER GOODIES",
            "section": "Method",
            "pages": [77],
        },
    )

    result = RetrievalResult(
        chunk=chunk,
        score=0.2,
        source="vector",
    )

    context = build_context([result])

    assert "[Source 1]" in context
    assert "Recipe: Carrot Halva" in context
    assert "Section: Method" in context
    assert "Pages: 77" in context
    assert "Clean and grate the carrots." in context
