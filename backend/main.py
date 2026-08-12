from pathlib import Path

from services.pdf_service import extract_pdf_text
from services.chunking_service import chunk_pages
from services.embedding_service import generate_embeddings
from services.vector_store_service import (
    get_chunk_count,
    store_chunks,
    search_vector_store,
)
from services.prompt_service import build_rag_prompt
from services.llm_service import generate_answer
from services.query_service import normalize_query


def main() -> None:
    """
    Main RAG pipeline.

    Flow:
    1. Index PDF if ChromaDB is empty
    2. Ask user a question
    3. Normalize the query for better retrieval
    4. Search ChromaDB
    5. Build RAG prompt using original question
    6. Generate final answer using Gemini
    """

    pdf_path = (
        Path(__file__).parent
        / "samples"
        / "sample1.pdf"
    )

    try:
        # ---------------------------------
        # STEP 1: Check vector database
        # ---------------------------------

        chunk_count = get_chunk_count()

        if chunk_count == 0:
            print("No indexed document found.")
            print("Processing PDF...\n")

            pages = extract_pdf_text(pdf_path)

            chunks = chunk_pages(pages)

            embedded_chunks = generate_embeddings(chunks)

            store_chunks(embedded_chunks)

            print(f"Pages extracted: {len(pages)}")
            print(f"Chunks stored: {len(embedded_chunks)}")

        else:
            print(
                f"Using existing vector store "
                f"with {chunk_count} chunks."
            )

        # ---------------------------------
        # STEP 2: User question
        # ---------------------------------

        query = input(
            "\nAsk a question about the PDF: "
        ).strip()

        if not query:
            raise ValueError("Question cannot be empty.")

        # ---------------------------------
        # STEP 3: Normalize query
        # ---------------------------------

        normalized_query = normalize_query(query)

        if normalized_query.lower() != query.lower():
            print(
                f"\nSearching for: "
                f"{normalized_query}"
            )

        # ---------------------------------
        # STEP 4: Retrieve relevant chunks
        # ---------------------------------

        search_results = search_vector_store(
            query=normalized_query,
            top_k=5,
        )

        # ---------------------------------
        # STEP 5: Build RAG prompt
        # ---------------------------------

        # Important:
        # Use ORIGINAL user question here,
        # not the normalized query.
        prompt = build_rag_prompt(
            query=query,
            search_results=search_results,
        )

        # ---------------------------------
        # STEP 6: Generate Gemini answer
        # ---------------------------------

        answer = generate_answer(prompt)

        # ---------------------------------
        # STEP 7: Display answer
        # ---------------------------------

        print("\n" + "=" * 70)
        print("ANSWER")
        print("=" * 70)

        print(answer)

        # ---------------------------------
        # STEP 8: Display retrieved sources
        # ---------------------------------

        source_pages = sorted(
            {
                result["metadata"]["page_number"]
                for result in search_results
            }
        )

        print("\nSources:")

        for page_number in source_pages:
            print(f"- Page {page_number}")

    except (
        FileNotFoundError,
        ValueError,
        RuntimeError,
        TypeError,
    ) as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()