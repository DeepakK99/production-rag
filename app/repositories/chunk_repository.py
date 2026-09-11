from sqlalchemy.orm import Session

from app.ingestion.chunker import Chunk
from app.models import Chunk as ChunkModel


def save_chunks(
    session: Session,
    document_id: int,
    chunks: list[Chunk],
) -> list[ChunkModel]:
    db_chunks = []

    for chunk in chunks:
        db_chunk = ChunkModel(
            document_id=document_id,
            content=chunk.content,
            chunk_index=chunk.chunk_index,
            metadata_={
                "recipe_number": chunk.recipe_number,
                "recipe_name": chunk.recipe_name,
                "chapter_number": chunk.chapter_number,
                "chapter_title": chunk.chapter_title,
                "section": chunk.section,
                "pages": chunk.pages,
            },
            embedding=chunk.embedding,
        )

        session.add(db_chunk)
        db_chunks.append(db_chunk)

    session.commit()

    return db_chunks
