import json
import os
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv

from datapizza.embedders.openai import OpenAIEmbedder
from datapizza.type import (
    Chunk,
    DenseEmbedding,
)

from rag.pdf_loader import load_pdf_text
from rag.qdrant_manager import ensure_collection

from rag.config import (
    COLLECTION_NAME,
    EMBEDDING_MODEL,
)

load_dotenv()


RULEBOOK_DIR = Path(
    "data/rulebooks"
)

MAPPING_FILE = (
    "data/catalog/rulebook_mapping.json"
)


def chunk_text(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 200,
):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(
            text[start:end]
        )

        start += chunk_size - overlap

    return chunks


def load_mapping():

    with open(
        MAPPING_FILE,
        encoding="utf-8"
    ) as f:

        return json.load(f)


def main():

    mapping = load_mapping()

    embedder = OpenAIEmbedder(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name=EMBEDDING_MODEL,
    )

    vectorstore = ensure_collection()

    pdfs = list(
        RULEBOOK_DIR.glob("*.pdf")
    )

    print(
        f"Trovati {len(pdfs)} PDF"
    )

    total_chunks = 0

    for pdf in pdfs:

        filename = pdf.name

        game = mapping.get(
            filename,
            filename.lower()
        )

        print()
        print(
            f"Processing: {filename}"
        )

        text = load_pdf_text(
            str(pdf)
        )

        pdf_chunks = chunk_text(text)

        print(
            f"Chunks: {len(pdf_chunks)}"
        )

        for chunk_text_value in pdf_chunks:

            vector = embedder.embed(
                chunk_text_value
            )

            embedded_chunk = Chunk(
                id=str(uuid4()),
                text=chunk_text_value,
                embeddings=[
                    DenseEmbedding(
                        name="text_embedding",
                        vector=vector,
                    )
                ],
                metadata={
                    "game": game,
                    "source_file": filename,
                },
            )

            vectorstore.add(
                chunk=embedded_chunk,
                collection_name=COLLECTION_NAME,
            )

            total_chunks += 1

    print()
    print(
        f"Ingestion completata."
    )
    print(
        f"Chunk caricati: {total_chunks}"
    )


if __name__ == "__main__":
    main()