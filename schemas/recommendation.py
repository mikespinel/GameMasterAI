from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    players: int = Field(..., ge=1)
    max_duration: int = Field(..., ge=10)

    complexity_max: int = Field(
        default=5,
        ge=1,
        le=5
    )

    cooperative: bool | None = None

    competitive: bool | None = None

    min_age: int = 0


class RecommendedGame(BaseModel):
    id: str
    name: str
    score: float
    description: str


class RecommendationResponse(BaseModel):
    games: list[RecommendedGame]