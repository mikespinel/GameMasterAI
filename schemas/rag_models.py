from pydantic import BaseModel


class RetrievedChunk(BaseModel):
    text: str
    source_file: str
    score: float


class RulebookAnswer(BaseModel):
    answer: str
    sources: list[str]