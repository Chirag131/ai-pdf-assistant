from services.pdf_services import extract_pdf_text
from pathlib import Path


def display_extracted_pages(pages: list[dict]) -> None:
    """Display extracted PDF pages in the terminal."""

    print(f"\nSuccessfully processed {len(pages)} page(s).\n")

    for page in pages :
        page_number = page['page_number']
        text = page['text']
        character_count = page["character_count"]

        print("=" * 70)
        print(f"PAGE {page_number}")
        print(f"CHARACTERS EXTRACTED: {character_count}")
        print("=" * 70)
        
        if text:
            print(text)
        else:
            print('No selectable text found on this page')
        print()

def main() -> None:
    pdf_path = Path(__file__).parent / "samples" / "sample1.pdf"

    try:
        pages = extract_pdf_text(pdf_path)
        display_extracted_pages(pages)

    except (FileNotFoundError, ValueError, RuntimeError) as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
