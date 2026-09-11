from dataclasses import dataclass

from app.models import Chunk


@dataclass
class RetrievalResult:
    chunk: Chunk
    distance: float

    @property
    def similarity(self) -> float:
        return 1.0 - self.distance
