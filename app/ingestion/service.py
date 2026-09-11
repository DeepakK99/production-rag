from app.database import SessionLocal
from app.ingestion.chunker import build_chunks
from app.ingestion.embedding import EmbeddingProvider, embed_chunks
from app.ingestion.grouping import group_by_recipe
from app.ingestion.models import DocumentElement, IngestionResult
from app.ingestion.normalizer import normalize_elements
from app.ingestion.parser import parse_pdf
from app.repositories.document_repository import save_ingestion_result


class IngestionService:
    def __init__(self, embedding_provider: EmbeddingProvider):
        self.embedding_provider = embedding_provider

    def ingest(
        self,
        elements: list[DocumentElement],
    ) -> IngestionResult:
        normalized_elements = normalize_elements(elements)

        recipes = group_by_recipe(normalized_elements)

        chunks = []

        for recipe in recipes:
            recipe_chunks = build_chunks(recipe)
            chunks.extend(recipe_chunks)

        chunks = embed_chunks(
            chunks,
            self.embedding_provider,
        )

        return IngestionResult(
            elements=normalized_elements,
            recipes=recipes,
            chunks=chunks,
        )


if __name__ == "__main__":
    from app.ingestion.embedding import OllamaEmbeddingProvider

    provider = OllamaEmbeddingProvider(
        model="nomic-embed-text:latest",
    )

    service = IngestionService(
        embedding_provider=provider,
    )

    elements = parse_pdf("data/Indian Recipes.pdf")

    result = service.ingest(elements)

    print("Normalized elements:", len(result.elements))
    print("Recipes:", len(result.recipes))
    print("Chunks:", len(result.chunks))

    for chunk in result.chunks:
        print(
            chunk.recipe_number,
            "|",
            chunk.recipe_name,
            "|",
            chunk.section,
            "|",
            len(chunk.embedding),
        )

    session = SessionLocal()

    try:
        document = save_ingestion_result(
            session=session,
            filename="Indian Recipes.pdf",
            result=result,
        )

        print("Document ID:", document.id)

    finally:
        session.close()
