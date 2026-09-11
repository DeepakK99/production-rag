from dataclasses import dataclass, field
from typing import Any


@dataclass
class DocumentElement:
    text: str
    element_type: str
    page_number: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RecipeDocument:
    recipe_number: str
    recipe_name: str
    chapter_number: int | None
    chapter_title: str | None
    elements: list[DocumentElement]

    @property
    def pages(self) -> list[int]:
        return sorted(
            {
                element.page_number
                for element in self.elements
                if element.page_number is not None
            }
        )


@dataclass
class Chunk:
    content: str
    chunk_index: int
    recipe_number: str
    recipe_name: str
    chapter_number: int | None
    chapter_title: str | None
    section: str | None
    pages: list[int]
    embedding: list[float] | None = None


@dataclass
class IngestionResult:
    elements: list[DocumentElement]
    recipes: list[RecipeDocument]
    chunks: list[Chunk]
