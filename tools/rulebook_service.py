import os

from datapizza.clients.openai import (
    OpenAIClient,
)
from datapizza.embedders.openai import (
    OpenAIEmbedder,
)
from datapizza.tools import tool
from dotenv import load_dotenv

from rag.config import (
    COLLECTION_NAME,
    EMBEDDING_MODEL,
)
from rag.qdrant_manager import (
    ensure_collection,
)

load_dotenv()

def ask_rulebook(
    question: str,
    top_k: int = 5,
):
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

    return {
        "answer": response.content[0].content,
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