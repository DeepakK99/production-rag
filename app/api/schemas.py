from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(min_length=1)


class CitationResponse(BaseModel):
    source_id: int
    recipe_number: str | None
    recipe_name: str | None
    section: str | None
    pages: list[int]


class QueryResponse(BaseModel):
    answer: str
    citations: list[CitationResponse]
