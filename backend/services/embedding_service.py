from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

_model = SentenceTransformer(MODEL_NAME)

def generate_embeddings(chunks: list[dict]) -> list[dict]:
    if not chunks:
        return []

    texts = [chunk["text"] for chunk in chunks]

    embeddings = _model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True,
        normalize_embeddings=True,
    )

    embedded_chunks: list[dict] = []

    for chunk, embedding in zip(chunks, embeddings):
        embedded_chunks.append(
            {
                **chunk,
                "embedding": embedding.tolist(),
            }
        )

    return embedded_chunks

def generate_query_embedding(query:str) -> list[float]:
    cleaned_query = query.strip()
    
    if not cleaned_query:
        raise ValueError("Query cannot be empty.")

    embedding = _model.encode(
        cleaned_query,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    
    return embedding.tolist()