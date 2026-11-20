import json

from schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
    RecommendedGame
)

def load_games():

    with open(
        "data/catalog/games.json",
        encoding="utf-8"
    ) as f:
        return json.load(f)

def calculate_score(
    game,
    request: RecommendationRequest,
):

    if not (
        game["min_players"]
        <= request.players
        <= game["max_players"]
    ):
        return 0

    if (
        request.cooperative is not None
        and game["cooperative"] != request.cooperative
    ):
        return 0

    if (
        request.competitive is not None
        and game["competitive"] != request.competitive
    ):
        return 0

    score = 5

    if game["play_time"] <= request.max_duration:
        score += 3

    complexity_delta = abs(
        game["complexity"] - request.complexity_max
    )

    score += max(
        0,
        3 - complexity_delta
    )

    return score

def recommend_games(
    request: RecommendationRequest,
) -> RecommendationResponse:

    games = load_games()

    ranked = []

    for game in games:

        score = calculate_score(
            game,
            request,
        )

        if score <= 0:
            continue

        ranked.append(
            RecommendedGame(
                id=game["id"],
                name=game["name"],
                description=game["description"],
                score=score
            )
        )

    ranked.sort(
        key=lambda x: x.score,
        reverse=True,
    )

    return RecommendationResponse(
        games=ranked[:5]
    )