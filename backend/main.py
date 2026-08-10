from pathlib import Path

from services.pdf_service import extract_pdf_text
from services.chunking_service import chunk_pages
from services.embedding_service import generate_embeddings
from services.vector_store_service import (
    store_chunks,
    search_vector_store,
    get_chunk_count,
)

def display_results(results: list[dict]) -> None:
    if not results:
        print("\nNo results found.")
        return

    print("\nMost relevant chunks:\n")

    for rank, result in enumerate(results, start=1):
        metadata = result["metadata"]

        print("=" * 70)
        print(f"RESULT {rank}")
        print(f"Chunk ID : {result['chunk_id']}")
        print(f"Page     : {metadata['page_number']}")
        print(f"Distance : {result['distance']:.4f}")
        print("=" * 70)
        print(result["text"])
        print()
        


def main() -> None:
    pdf_path = Path(__file__).parent / "samples" / "sample1.pdf"

    try:
        chunk_count = get_chunk_count()

        if chunk_count == 0:
            print("No indexed document found. Processing PDF...")

            pages = extract_pdf_text(pdf_path)
            chunks = chunk_pages(pages)
            embedded_chunks = generate_embeddings(chunks)

            store_chunks(embedded_chunks)

            print(f"Pages extracted: {len(pages)}")
            print(f"Chunks stored: {len(embedded_chunks)}")

        else:
            print(f"Using existing vector store with {chunk_count} chunks.")

        query = input("\nAsk a question about the PDF: ")

        results = search_vector_store(
            query=query,
            top_k=3,
        )

        display_results(results)

    except (
        FileNotFoundError,
        ValueError,
        RuntimeError,
        TypeError,
    ) as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()