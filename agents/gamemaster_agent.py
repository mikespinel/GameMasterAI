from datapizza.agents import Agent

from agents.recommendation_agent import (
    game_recommendation_tool,
)
from prompts.gamemaster_prompt import (
    SYSTEM_PROMPT,
)
from tools.rulebook_tool import (
    rulebook_tool,
)


def create_gamemaster_agent(
    client,
):

    return Agent(
        name="GameMasterAgent",
        client=client,
        system_prompt=SYSTEM_PROMPT,
        tools=[
            game_recommendation_tool,
            rulebook_tool,
        ],
    )