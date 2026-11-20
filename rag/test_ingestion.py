from pathlib import Path

from rag.pdf_loader import (
    load_pdf_text
)

from rag.chunker import (
    create_chunks
)

pdf = (
    "data/rulebooks/"
    "ITA-Rules-Pandemic.pdf"
)

text = load_pdf_text(pdf)

print()
print("CARATTERI:")
print(len(text))

chunks = create_chunks(
    text=text,
    game="pandemic",
    source_file="ITA-Rules-Pandemic.pdf",
)

print()
print("CHUNKS:")
print(len(chunks))

print()
print("PRIMO CHUNK:")
print(chunks[0].text[:500])

print()

print(chunks[0].metadata)