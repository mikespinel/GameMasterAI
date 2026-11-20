from tools.rulebook_tool import (
    ask_rulebook
)

def test_rulebook_answer():

    result = ask_rulebook(
        "Come si diffondono le malattie?"
    )

    assert result["answer"]