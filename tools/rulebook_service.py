import os

from datapizza.clients.openai import (
    OpenAIClient,
)
from datapizza.embedders.openai import (
    OpenAIEmbedder,
)
from datapizza.tools import tool
from dotenv import load_dotenv

from memory.conversation_state import (
    conversation_state,
)
from rag.config import (
    COLLECTION_NAME,
    EMBEDDING_MODEL,
)
from rag.game_detector import (
    detect_game,
)
from rag.qdrant_manager import (
    ensure_collection,
)

load_dotenv()

def ask_rulebook(
    question: str,
    top_k: int = 5,
):
    detected_game = detect_game(
        question
    )

    if detected_game:

        conversation_state.set_game(
            detected_game
        )

    current_game = (
        conversation_state.get_game()
    )

    print(
        "CURRENT GAME:",
        current_game
    )

    used_game = current_game
 
    embedder = OpenAIEmbedder(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name=EMBEDDING_MODEL,
    )

    query_vector = embedder.embed(
        question
    )

    store = ensure_collection()

    chunks = store.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        k=top_k,
        vector_name="text_embedding",
    )

    if current_game:

        chunks = [
            chunk
            for chunk in chunks
            if chunk.metadata.get("game")
            == current_game
        ]

    games_found = {}

    for chunk in chunks:

        game = chunk.metadata.get(
            "game"
        )

        if game:

            games_found[game] = (
                games_found.get(game, 0)
                + 1
            )
            

    if (
        used_game is None
        and games_found
    ):

        used_game = max(
            games_found,
            key=games_found.get
        )

        conversation_state.set_game(
            used_game
        )

    context = "\n\n".join(
        chunk.text
        for chunk in chunks
    )

    sources = list(
        {
            chunk.metadata[
                "source_file"
            ]
            for chunk in chunks
        }
    )

    prompt = f"""
    Rispondi usando ESCLUSIVAMENTE le informazioni presenti nel contesto.

    Se non trovi la risposta:
    rispondi "Non ho trovato l'informazione nei regolamenti caricati".

    CONTESTO:

    {context}

    DOMANDA:

    {question}
    """

    client = OpenAIClient(
        api_key=os.getenv(
            "OPENAI_API_KEY"
        ),
        model="gpt-4o-mini",
    )
    response = client.invoke(
        prompt
    )

    intro = ""

    if current_game is None and used_game:

        intro = (
            f"Deduco che tu stia parlando di "
            f"{used_game.replace('_', ' ').title()}.\n\n"
            f"Se non è il gioco corretto, indicamelo.\n\n"
        )

    return {
        "answer": (
            intro + response.content[0].content
        ),
        "sources": sources,
    }



@tool
def rulebook_tool(
    question: str,
):
    """
    Interroga i regolamenti caricati.
    """

    result = ask_rulebook(
        question=question,
    )

    return str(result)