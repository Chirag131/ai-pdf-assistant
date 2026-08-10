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

def get_chunk_count() -> int:
    return collection.count()
 
def search_vector_store(
    query: str,
    top_k: int = 3,
) -> list[dict]:
    if top_k <= 0:
        raise ValueError("top_k must be greater than 0")

    query_embedding = generate_query_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    search_results = []

    for index in range(len(results["ids"][0])):
        search_results.append(
            {
                "chunk_id": results["ids"][0][index],
                "text": results["documents"][0][index],
                "metadata": results["metadatas"][0][index],
                "distance": results["distances"][0][index],
            }
        )

    return search_results