def chunk_pages(
    pages: list[dict],
    chunk_size: int = 800,
    overlap: int = 150,
) -> list[dict]:
    """
    Split extracted PDF pages into overlapping character-based chunks.
    """

    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    if overlap < 0:
        raise ValueError("Overlap cannot be negative.")

    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk size.")

    chunks: list[dict] = []

    for page in pages:
        page_number = page["page_number"]

        # Keep the page content as a string.
        text = page["text"].strip()

        if not text:
            continue

        start = 0
        chunk_index = 1
        step = chunk_size - overlap

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            if chunk_text.strip():
                chunks.append(
                    {
                        "chunk_id": f"page_{page_number}_chunk_{chunk_index}",
                        "page_number": page_number,
                        "chunk_index": chunk_index,
                        "text": chunk_text,
                        "character_count": len(chunk_text),
                    }
                )

            start += step
            chunk_index += 1

    return chunks