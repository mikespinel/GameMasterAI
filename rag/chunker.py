import uuid

from datapizza.type import Chunk

CHUNK_SIZE = 1200
OVERLAP = 200


def create_chunks(
    text: str,
    game: str,
    source_file: str,
):

    chunks = []

    start = 0

    while start < len(text):

        end = start + CHUNK_SIZE

        chunk_text = text[start:end]

        chunk = Chunk(
            id=str(uuid.uuid4()),
            text=chunk_text,
            metadata={
                "game": game,
                "source_file": source_file,
            },
        )

        chunks.append(chunk)

        start += CHUNK_SIZE - OVERLAP

    return chunks