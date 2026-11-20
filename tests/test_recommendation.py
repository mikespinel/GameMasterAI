from schemas.recommendation import RecommendationRequest
from tools.recommendation_tool import recommend_games


def test_coop_games():

    request = RecommendationRequest(
        players=4,
        max_duration=60,
        cooperative=True,
        complexity_max=3,
        min_age=12
    )

    result = recommend_games(request)

    assert len(result.games) > 0

def test_pandemic_is_candidate():

    request = RecommendationRequest(
        players=4,
        cooperative=True,
        max_duration=60
    )

    result = recommend_games(request)

    names = [
        g.name
        for g in result.games
    ]

    assert "Pandemic" in names

def test_returns_games():

    request = RecommendationRequest(
        players=4,
        max_duration=90,
    )

    result = recommend_games(request)

    assert len(result.games) > 0

def test_no_invalid_player_count():

    request = RecommendationRequest(
        players=20,
        max_duration=60,
    )

    result = recommend_games(request)

    assert len(result.games) == 0

def test_two_players():

    request = RecommendationRequest(
        players=2,
        max_duration=60,
        competitive=True
    )

    result = recommend_games(request)

    names = [g.name for g in result.games]

    assert "7 Wonders Duel" in names