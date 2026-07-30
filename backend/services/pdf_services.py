from pathlib import Path
import pymupdf

def extract_pdf_text(pdf_path: Path) -> list[dict]:
    """
    Extract text from a PDF page by page.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        A list containing page numbers and extracted text.

    Raises:
        FileNotFoundError: If the PDF does not exist.
        ValueError: If the supplied file is not a PDF.
        RuntimeError: If PyMuPDF cannot process the document.
    """

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    if not pdf_path.is_file():
        raise ValueError(f"Invalid Path: {pdf_path}")
    
    if pdf_path.suffix.lower() != '.pdf':
        raise ValueError("Only Pdf supported")

    extracted_pages : list[dict] = []
    
    try :
        with pymupdf.open(pdf_path) as document:
            if document.page_count == 0 :
                raise ValueError('Empty PDF')
            
            for page_index, page in enumerate(document):
                page_number = page_index + 1

                # sort=True attempts to return text in reading order.
                text = page.get_text("text", sort=True).strip()
                
                extracted_pages.append(
                    {
                        "page_number" : page_number,
                        "text" : text,
                        "character_count" : len(text),
                    }
                )
                
    except pymupdf.FileDataError as error:
        raise RuntimeError(
            "The PDF could not be opened. It may be corrupted or invalid."
        ) from error

    return extracted_pages