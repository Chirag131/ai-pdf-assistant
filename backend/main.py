from services.pdf_services import extract_pdf_text
from services.chunking_service import chunk_pages
from pathlib import Path
    
def main() -> None:
    pdf_path = Path(__file__).parent / "samples" / "sample1.pdf"

    try:
        pages = extract_pdf_text(pdf_path)
        chunks = chunk_pages(pages)

        print(f"Pages extracted: {len(pages)}")
        print(f"Chunks created: {len(chunks)}")

        for chunk in chunks[:5]:
            print("=" * 70)
            print(chunk["chunk_id"])
            print(f"Page: {chunk['page_number']}")
            print(f"Characters: {chunk['character_count']}")
            print("=" * 70)
            print(chunk["text"])
            print()

    except (FileNotFoundError, ValueError, RuntimeError) as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    main()
