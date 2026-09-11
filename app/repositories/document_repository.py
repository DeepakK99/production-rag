from sqlalchemy.orm import Session

from app.ingestion.models import IngestionResult
from app.models import Chunk as ChunkModel
from app.models import Document


def save_ingestion_result(
    session: Session,
    filename: str,
    result: IngestionResult,
) -> Document:
    try:
        document = Document(
            filename=filename,
        )

        session.add(document)
        session.flush()

        for chunk in result.chunks:
            db_chunk = ChunkModel(
                document_id=document.id,
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

        session.commit()
        session.refresh(document)

        return document

    except Exception:
        session.rollback()
        raise
