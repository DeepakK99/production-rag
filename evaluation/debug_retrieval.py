from app.database import SessionLocal
from app.ingestion.embedding import OllamaEmbeddingProvider
from app.retrieval.retriever import search_similar_chunks
from app.retrieval.keyword_retriever import search_keyword_chunks
from app.retrieval.hybrid import reciprocal_rank_fusion


embedding_provider = OllamaEmbeddingProvider(
    model="nomic-embed-text:latest",
)

question = "What ingredients are needed for Coriander Fish?"
question_with_or = ' OR '.join(question.split())
from sqlalchemy.sql import text
with SessionLocal() as session:
    rows = session.execute(
        text("""
            SELECT
                id,
                metadata->>'recipe_name' AS recipe,
                metadata->>'section' AS section,
                ts_rank_cd(
                    search_vector,
                    websearch_to_tsquery(
                        'english',
                        :query
                    )
                ) AS rank
            FROM chunks
            WHERE search_vector @@ websearch_to_tsquery(
                'english',
                :query
            )
            ORDER BY rank DESC
            LIMIT 10
        """),
        {"query": question_with_or},
    ).all()

    for row in rows:
        print(row)

exit(0)


with SessionLocal() as session:
    
    query_embedding = embedding_provider.embed(question)

    vector_results = search_similar_chunks(
        session=session,
        query_embedding=query_embedding,
        limit=5,
    )

    keyword_results = search_keyword_chunks(
        session=session,
        query=question,
        limit=5,
    )

    hybrid_results = reciprocal_rank_fusion(
        [
            vector_results,
            keyword_results,
        ]
    )[:5]

    print("\n=== VECTOR RESULTS ===")

    for rank, result in enumerate(vector_results, start=1):
        metadata = result.chunk.metadata_

        print(
            f"{rank}. "
            f"{metadata.get('recipe_number')} "
            f"{metadata.get('recipe_name')} "
            f"[{metadata.get('section')}] "
            f"score={result.score:.4f}"
        )

    print("\n=== KEYWORD RESULTS ===")

    for rank, result in enumerate(keyword_results, start=1):
        metadata = result.chunk.metadata_

        print(
            f"{rank}. "
            f"{metadata.get('recipe_number')} "
            f"{metadata.get('recipe_name')} "
            f"[{metadata.get('section')}] "
            f"score={result.score:.4f}"
        )

    print("\n=== HYBRID RESULTS ===")

    for rank, result in enumerate(hybrid_results, start=1):
        metadata = result.chunk.metadata_

        print(
            f"{rank}. "
            f"{metadata.get('recipe_number')} "
            f"{metadata.get('recipe_name')} "
            f"[{metadata.get('section')}] "
            f"RRF={result.score:.4f}"
        )