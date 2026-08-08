from pathlib import Path

from services.chunking_service import chunk_pages
from services.embedding_service import generate_embeddings
from services.pdf_service import extract_pdf_text
from services.retrieval_service import search_similar_chunks


def display_search_results(results: list[dict]) -> None:
    if not results:
        print("\nNo results found.")
        return

    print("\nMost relevant chunks:\n")

    for rank, result in enumerate(results, start=1):
        print("=" * 70)
        print(f"RESULT {rank}")
        print(f"Chunk: {result['chunk_id']}")
        print(f"Page: {result['page_number']}")
        print(f"Similarity: {result['similarity_score']:.4f}")
        print("=" * 70)
        print(result["text"])
        print()


def main() -> None:
    pdf_path = Path(__file__).parent / "samples" / "sample1.pdf"

    try:
        pages = extract_pdf_text(pdf_path)
        chunks = chunk_pages(pages)
        embedded_chunks = generate_embeddings(chunks)

        print(f"\nPages extracted: {len(pages)}")
        print(f"Chunks created: {len(chunks)}")
        print(f"Embeddings generated: {len(embedded_chunks)}")

        query = input("\nAsk a question about the PDF: ")

        results = search_similar_chunks(
            query=query,
            embedded_chunks=embedded_chunks,
            top_k=5,
        )

        display_search_results(results)

    except (
        FileNotFoundError,
        ValueError,
        RuntimeError,
        TypeError,
    ) as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()