from fastapi.testclient import TestClient

from app.api.routes import get_rag_service
from app.generation.service import RAGResponse
from app.main import app
from app.retrieval.citations import Citation


class FakeRAGService:
    def query(self, session, question, limit=5):
        return RAGResponse(
            answer="This is a test answer.",
            citations=[
                Citation(
                    source_id=42,
                    recipe_number="12.8",
                    recipe_name="Carrot Halva",
                    section="Method",
                    pages=[77, 78],
                )
            ],
        )


def get_fake_rag_service():
    return FakeRAGService()


def test_query_endpoint():
    app.dependency_overrides[get_rag_service] = get_fake_rag_service

    client = TestClient(app)

    response = client.post(
        "/query",
        json={"question": "How do I make carrot halva?"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == "This is a test answer."

    assert data["citations"] == [
        {
            "source_id": 42,
            "recipe_number": "12.8",
            "recipe_name": "Carrot Halva",
            "section": "Method",
            "pages": [77, 78],
        }
    ]

    app.dependency_overrides.clear()
