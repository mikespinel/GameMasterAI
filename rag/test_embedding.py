import os

from dotenv import load_dotenv

from datapizza.embedders.openai import (
    OpenAIEmbedder
)

from rag.pdf_loader import (
    load_pdf_text
)

from rag.chunker import (
    create_chunks
)

load_dotenv()

pdf = (
    "data/rulebooks/"
    "ITA-Rules-Pandemic.pdf"
)

text = load_pdf_text(pdf)

chunks = create_chunks(
    text=text,
    game="pandemic",
    source_file="ITA-Rules-Pandemic.pdf",
)

print()
print("chunks:", len(chunks))
print()

embedder = OpenAIEmbedder(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small",
)

embedding = embedder.embed(
    chunks[0].text
)

print(type(embedding))
print()

print(embedding)