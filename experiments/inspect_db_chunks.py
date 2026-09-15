# from app.database import SessionLocal
# from app.models import Chunk


# with SessionLocal() as session:
#     chunks = session.query(Chunk).order_by(Chunk.chunk_index).all()

#     for chunk in chunks:
#         metadata = chunk.metadata_

#         print(
#             chunk.id,
#             " | ",
#             metadata.get("recipe_number"),
#             " | ",
#             metadata.get("recipe_name"),
#             " | ",
#             metadata.get("section"),
#         )


from sqlalchemy import select

from app.database import SessionLocal
from app.models import Chunk

with SessionLocal() as session:
    statement = (
        select(Chunk)
        .where(Chunk.metadata_["recipe_number"].as_string() == "4.3")
        .order_by(Chunk.id)
    )

    chunks = session.execute(statement).scalars().all()

    for chunk in chunks:
        print(
            chunk.id,
            chunk.metadata_.get("recipe_number"),
            chunk.metadata_.get("recipe_name"),
            chunk.metadata_.get("section"),
        )
