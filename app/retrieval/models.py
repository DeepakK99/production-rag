from dataclasses import dataclass

from app.models import Chunk


@dataclass
class RetrievalResult:
    chunk: Chunk
    score: float
    source: str
