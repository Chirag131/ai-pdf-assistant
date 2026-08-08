import math

from services.embedding_service import generate_query_embedding

def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float :
    if not vector_a or not vector_b :
        raise ValueError("Vectors cannot be empty")
    
    if len(vector_a) != len(vector_b):
        raise ValueError("Vectors must be same size")
    
    dot_product = sum(
        value_a * value_b
        for value_a, value_b in zip(vector_a, vector_b)
    )
    
    magnitude_a = math.sqrt(sum(value * value for value in vector_a))
    
    magnitude_b = math.sqrt(sum(value * value for value in vector_b))
    
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    
    return dot_product/(magnitude_a * magnitude_b)

def search_similar_chunks(
    query: str,
    embedded_chunks: list[dict],
    top_k: int = 3,
    
) -> list[dict]:
    if top_k <= 0 :
        raise ValueError("top_k must be greater than zero")
    
    if not embedded_chunks :
        return []
    
    query_embedding = generate_query_embedding(query)
    
    scored_chunks: list[dict] = []
    
    for chunk in embedded_chunks:
        embedding = chunk.get("embedding")

        if embedding is None :
            continue
        
        similarity_score = cosine_similarity(
            query_embedding,
            embedding,
        )

        scored_chunks.append({
            "chunk_id": chunk["chunk_id"],
            "page_number": chunk["page_number"],
            "chunk_index": chunk["chunk_index"],
            "text": chunk["text"],
            "character_count": chunk["character_count"],
            "similarity_score": similarity_score,
        })
        
        scored_chunks.sort(
            key = lambda item: item["similarity_score"],
            reverse=True,
        )
        
    return scored_chunks[:top_k]
    
    