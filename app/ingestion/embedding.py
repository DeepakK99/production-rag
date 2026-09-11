from typing import Protocol

import ollama

from app.ingestion.chunker import Chunk


class EmbeddingProvider(Protocol):
    def embed(self, text: str) -> list[float]: ...


class OllamaEmbeddingProvider:
    def __init__(self, model: str):
        self.model = model

    def embed(self, text: str) -> list[float]:
        response = ollama.embed(
            model=self.model,
            input=text,
        )

        return response["embeddings"][0]


def embed_chunks(
    chunks: list[Chunk],
    provider: EmbeddingProvider,
) -> list[Chunk]:
    for chunk in chunks:
        chunk.embedding = provider.embed(chunk.content)

    return chunks
