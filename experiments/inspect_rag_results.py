from app.database import SessionLocal
from app.generation.llm import OllamaLLMProvider
from app.generation.service import RAGService
from app.ingestion.embedding import OllamaEmbeddingProvider
from app.retrieval.retriever import search_similar_chunks

embedding_provider = OllamaEmbeddingProvider(
    model="nomic-embed-text:latest ",
)

llm_provider = OllamaLLMProvider(
    model="gemma3:4b",
)

query = "How do I make carrot halva?"

query_embedding = embedding_provider.embed(query)

with SessionLocal() as session:
    results = search_similar_chunks(
        session=session,
        query_embedding=query_embedding,
        limit=5,
    )

rag = RAGService(llm_provider)

answer = rag.answer(
    question=query,
    results=results,
)

print(answer)
