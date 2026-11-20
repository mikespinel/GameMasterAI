from datapizza.agents import Agent
from datapizza.tools import tool
from prompts.recommendation_prompt import SYSTEM_PROMPT

from schemas.recommendation import RecommendationRequest
from tools.recommendation_tool import recommend_games


@tool
def game_recommendation_tool(
    players: int,
    duration: int,
    complexity: int,
    cooperative: bool | None = None,
    competitive: bool | None = None,
):
    """
    Trova i giochi migliori dal catalogo.
    """

    request = RecommendationRequest(
        players=players,
        max_duration=duration,
        complexity_max=complexity,
        cooperative=cooperative,
        competitive=competitive,
        min_age=18,
    )

    result = recommend_games(request)

    return result.model_dump_json()


def create_recommendation_agent(client):

    return Agent(
    name="GameMasterRecommendationAgent",
    client=client,
    system_prompt=SYSTEM_PROMPT,
    tools=[game_recommendation_tool],
)
