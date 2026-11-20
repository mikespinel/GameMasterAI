import json


CATALOG_PATH = (
    "data/catalog/games.json"
)


def load_games():

    with open(
        CATALOG_PATH,
        encoding="utf-8"
    ) as f:

        return json.load(f)


def detect_game(
    question: str,
):

    question = question.lower()

    games = load_games()

    for game in games:

        if game["name"].lower() in question:

            return game["id"]

    return None