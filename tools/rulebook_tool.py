from datapizza.tools import tool

from tools.rulebook_service import (
    ask_rulebook,
)


@tool
def rulebook_tool(
    question: str,
):
    """
    Interroga i regolamenti caricati.
    """

    result = ask_rulebook(
        question=question
    )

    return str(result)