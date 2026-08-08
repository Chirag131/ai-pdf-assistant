from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

def generate_embeddings(chunks : list[dict]) -> list[dict] :
    """
    Generate an embedding for every text chunk.

    Args:
        chunks: Document chunks containing text and metadata.

    Returns:
        The chunks with an embedding added to each one.
    """
    if not chunks:
        return []
    
    model = SentenceTransformer(MODEL_NAME)
    
    texts = [chunk["text"] for chunk in chunks]
    
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True,
    )
    
    embedded_chunks: list[dict] = []
    
    for chunk,embedding in zip(chunks,embeddings):
        embedded_chunks.append(
            {
                **chunk,
                "embedding" : embedding.tolist(),
            }
        ) 
        
    return embedded_chunks
