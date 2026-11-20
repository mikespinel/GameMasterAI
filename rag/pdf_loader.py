import pymupdf


def load_pdf_text(
    pdf_path: str
):

    doc = pymupdf.open(pdf_path)

    pages = []

    for page in doc:

        pages.append(
            page.get_text()
        )

    return "\n".join(pages)