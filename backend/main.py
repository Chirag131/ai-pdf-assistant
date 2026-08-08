from pathlib import Path

from services.pdf_service import extract_pdf_text
from services.chunking_service import chunk_pages
from services.embedding_service import generate_embeddings


def main() -> None:
    pdf_path = Path("samples/sample1.pdf")

    pages = extract_pdf_text(pdf_path)
    chunks = chunk_pages(pages)
    embedded_chunks = generate_embeddings(chunks)

    print(f"Pages extracted: {len(pages)}")
    print(f"Chunks created: {len(chunks)}")
    print(f"Embeddings generated: {len(embedded_chunks)}")

    if embedded_chunks:
        first_chunk = embedded_chunks[0]

        print("\nFirst chunk:")
        print(first_chunk["text"][:200])

        print("\nEmbedding information:")
        print(f"Vector size: {len(first_chunk['embedding'])}")
        print(f"First 10 values: {first_chunk['embedding'][:10]}")


if __name__ == "__main__":
    main()