from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.generation.llm import LLMProvider
from app.ingestion.embedding import EmbeddingProvider
from app.retrieval.citations import Citation, build_citations
from app.retrieval.context import build_context
from app.retrieval.hybrid import search_hybrid_chunks
from app.retrieval.models import RetrievalResult
from app.reranking.models import Reranker


@dataclass
class RAGResponse:
    answer: str
    citations: list[Citation]


class RAGService:
    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        llm_provider: LLMProvider,
        reranker: Reranker,
    ):
        self.embedding_provider = embedding_provider
        self.llm_provider = llm_provider
        self.reranker = reranker

    def query(
        self,
        session: Session,
        question: str,
        candidate_limit: int = 50,
        final_limit: int = 5,
    ) -> RAGResponse:
        query_embedding = self.embedding_provider.embed(question)

        results = search_hybrid_chunks(
            session=session,
            query=question,
            query_embedding=query_embedding,
            candidate_limit=candidate_limit,
        )

        reranked_results = self.reranker.rerank(
            query=question,
            results=results,
        )

        return self.answer(
            question=question,
            results=reranked_results[:final_limit],
        )

    def answer(
        self,
        question: str,
        results: list[RetrievalResult],
    ) -> RAGResponse:
        context = build_context(results)

        prompt = f"""You are a helpful recipe assistant.

Answer the user's question using only the provided context.

Use citations in the form [1], [2], etc. when making factual claims.
Each citation number corresponds to the source with the same number
in the provided context.
Only use citation numbers that exist in the provided context.
Do not invent citation numbers.

If the context does not contain enough information to answer the question,
say that you don't have enough information.

Context:
{context}

User question:
{question}

Answer:
""".strip()

        answer = self.llm_provider.generate(prompt)

        return RAGResponse(
            answer=answer,
            citations=build_citations(results),
        )
