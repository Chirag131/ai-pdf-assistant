from pathlib import Path

import chromadb

from services.embedding_service import generate_query_embedding

CHROMA_PATH = Path(__file__).parent.parent/"chroma_data"
COLLECTION_NAME = "pdf_chunks"

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=None,
)

def store_chunks(embedded_chunks: list[dict]) -> None :
    if not embedded_chunks:
        return
    
    ids = []
    documents = [] 
    embeddings = []
    metadatas = []
    
    for chunk in embedded_chunks:
        ids.append(chunk["chunk_id"])
        documents.append(chunk["text"])
        embeddings.append(chunk["embedding"])

        metadatas.append(
            {
                "page_number": chunk["page_number"],
                "chunk_index": chunk["chunk_index"],
                "character_count": chunk["character_count"],
            }
        )
        
    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )
