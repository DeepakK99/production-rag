from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas import CitationResponse, QueryRequest, QueryResponse
from app.database import SessionLocal
from app.generation.llm import OllamaLLMProvider
from app.generation.service import RAGService
from app.ingestion.embedding import OllamaEmbeddingProvider

router = APIRouter()


def get_db():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


embedding_provider = OllamaEmbeddingProvider(
    model="nomic-embed-text:latest",
)

llm_provider = OllamaLLMProvider(
    model="gemma3:4b",
)


def get_rag_service() -> RAGService:
    return RAGService(
        embedding_provider=embedding_provider,
        llm_provider=llm_provider,
    )


@router.post("/query", response_model=QueryResponse)
def query(
    request: QueryRequest,
    session: Session = Depends(get_db),
    rag_service: RAGService = Depends(get_rag_service),
):
    try:
        response = rag_service.query(
            session=session,
            question=request.question,
        )

        citations = [
            CitationResponse(
                source_id=citation.source_id,
                recipe_number=citation.recipe_number,
                recipe_name=citation.recipe_name,
                section=citation.section,
                pages=citation.pages,
            )
            for citation in response.citations
        ]

        return QueryResponse(
            answer=response.answer,
            citations=citations,
        )
    except ConnectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI model engine is unreachable. Please ensure Ollama is running.",
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
