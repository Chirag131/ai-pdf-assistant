from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile, File

from app.schemas.chat import AskRequest, AskResponse
from app.schemas.upload import UploadResponse

from services.pdf_service import extract_pdf_text
from services.chunking_service import chunk_pages
from services.embedding_service import generate_embeddings
from services.vector_store_service import (
    store_chunks,
    search_vector_store,
)

from services.llm_service import generate_answer
from services.prompt_service import build_rag_prompt
from services.query_service import normalize_query


router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):

    try:

        # -----------------------------
        # Validate file
        # -----------------------------

        if not file.filename:
            raise ValueError("No file provided.")

        if not file.filename.lower().endswith(".pdf"):
            raise ValueError("Only PDF files are supported.")

        # -----------------------------
        # Save PDF temporarily
        # -----------------------------

        samples_dir = (
            Path(__file__).parent.parent.parent
            / "samples"
        )

        samples_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        pdf_path = samples_dir / file.filename

        contents = await file.read()

        with open(pdf_path, "wb") as pdf_file:
            pdf_file.write(contents)

        # -----------------------------
        # Extract text
        # -----------------------------

        pages = extract_pdf_text(pdf_path)

        # -----------------------------
        # Chunk text
        # -----------------------------

        chunks = chunk_pages(pages)

        # -----------------------------
        # Generate embeddings
        # -----------------------------

        embedded_chunks = generate_embeddings(
            chunks
        )

        # -----------------------------
        # Store in ChromaDB
        # -----------------------------

        store_chunks(
            embedded_chunks
        )

        return UploadResponse(
            filename=file.filename,
            pages_extracted=len(pages),
            chunks_created=len(embedded_chunks),
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:

        print("UPLOAD ERROR:", repr(error))

        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error


@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):

    try:

        question = request.question.strip()

        if not question:
            raise ValueError(
                "Question cannot be empty."
            )

        normalized_query = normalize_query(
            question
        )

        search_results = search_vector_store(
            query=normalized_query,
            top_k=5,
        )

        prompt = build_rag_prompt(
            query=question,
            search_results=search_results,
        )

        answer = generate_answer(prompt)

        source_pages = sorted(
            {
                result["metadata"]["page_number"]
                for result in search_results
            }
        )

        return AskResponse(
            answer=answer,
            sources=source_pages,
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:

        print("ASK ERROR:", repr(error))

        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error