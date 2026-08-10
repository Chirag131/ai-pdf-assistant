from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

# Load the model only once when this file is imported
_model = SentenceTransformer(MODEL_NAME)


def generate_embeddings(chunks: list[dict]) -> list[dict]:
    """
    Generate an embedding for every text chunk.

    Args:
        chunks: Document chunks containing text and metadata.

    Returns:
        The chunks with an embedding added to each one.
    """

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


def generate_query_embedding(query: str) -> list[float]:
    """
    Convert a user's query into an embedding vector.
    """

    cleaned_query = query.strip()

    if not cleaned_query:
        raise ValueError("Query cannot be empty.")

    embedding = _model.encode(
        cleaned_query,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    return embedding.tolist()