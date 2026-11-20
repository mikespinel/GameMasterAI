import os

from dotenv import load_dotenv

from datapizza.embedders.openai import (
    OpenAIEmbedder,
)

from rag.config import (
    COLLECTION_NAME,
    EMBEDDING_MODEL,
)

from rag.qdrant_manager import (
    ensure_collection,
)

load_dotenv()


def search_rulebooks(
    query: str,
    k: int = 5,
):

    embedder = OpenAIEmbedder(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name=EMBEDDING_MODEL,
    )

    vector = embedder.embed(query)

    store = ensure_collection()

    results = store.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        k=k,
        vector_name="text_embedding",
    )

    return results


if __name__ == "__main__":

    query = input("Domanda: ")

    results = search_rulebooks(query)

    print()
    print("RISULTATI")
    print()

    for i, chunk in enumerate(results, start=1):

        print("=" * 80)

        print(f"RISULTATO {i}")

        print()

        print(chunk.metadata)

        print()

        print(chunk.text[:800])

        print()