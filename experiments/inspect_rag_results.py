from app.database import SessionLocal
from app.ingestion.embedding import OllamaEmbeddingProvider
from app.retrieval.retriever import search_similar_chunks

query = "Carrot Halva"

provider = OllamaEmbeddingProvider(
    model="nomic-embed-text:latest",
)

query_embedding = provider.embed(query)

session = SessionLocal()

try:
    results = search_similar_chunks(
        session,
        query_embedding,
        limit=5,
    )

    for result in results:
        print(
            result.chunk.metadata_["recipe_name"],
            result.chunk.metadata_["section"],
            result.distance,
            result.similarity,
        )

finally:
    session.close()
