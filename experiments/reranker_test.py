from app.database import SessionLocal
from app.ingestion.embedding import OllamaEmbeddingProvider
from app.retrieval.hybrid import search_hybrid_chunks
from app.reranking.cross_encoder import CrossEncoderReranker


embedding_provider = OllamaEmbeddingProvider(
    model="nomic-embed-text:latest",
)

reranker = CrossEncoderReranker(
    model="cross-encoder/ms-marco-MiniLM-L-6-v2",
)

question = "What ingredients are needed for Coriander Fish?"
print("Question: ", question)

n = 10

with SessionLocal() as session:
    query_embedding = embedding_provider.embed(question)

    candidates = search_hybrid_chunks(
        session=session,
        query=question,
        query_embedding=query_embedding,
        candidate_limit=50,
    )

    print("\n=== BEFORE RERANKING) ===")
    print(f"=== Total candidates: {len(candidates)} ===")
    print(f"=== Showing: {n} ===")

    for rank, result in enumerate(candidates[:n], start=1):
        metadata = result.chunk.metadata_

        print(
            f"{rank}. "
            f"{metadata.get('recipe_number')} "
            f"{metadata.get('recipe_name')} "
            f"[{metadata.get('section')}] "
            f"RRF={result.score:.4f}"
        )

    reranked = reranker.rerank(
        query=question,
        results=candidates,
    )

    print("\n=== AFTER RERANKING ===")
    print(f"=== Total reranked: {len(reranked)} ===")
    print(f"=== Showing: {n} ===")

    for rank, result in enumerate(reranked[:n], start=1):
        metadata = result.chunk.metadata_

        print(
            f"{rank}. "
            f"{metadata.get('recipe_number')} "
            f"{metadata.get('recipe_name')} "
            f"[{metadata.get('section')}] "
            f"Reranker={result.score:.4f}"
        )