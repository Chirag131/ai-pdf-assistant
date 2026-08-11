def build_rag_prompt(
    query:str,
    search_results:list[dict],
) -> str:
    
    if not query.strip():
        raise ValueError("Query cannot be empty.")
    
    if not search_results:
        return (
            "No relevant document context was found.\n\n"
            f"Question: {query}"
        )
        
    context_parts = []
    
    for result in search_results:
        page_number = result["metadata"]["page_number"]
        text = result['text']
        
        context_parts.append(
            f"[Page {page_number}]\n{text}"
        )
        
    context = "\n\n".join(context_parts)
    
    return f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the document context below.

Rules:
1. Do not use outside knowledge.
2. If the answer is not supported by the context, say:
   "I could not find this information in the document."
3. Give a clear and concise answer.
4. Mention the relevant page number(s).
5. Do not invent facts.

DOCUMENT CONTEXT:

{context}

USER QUESTION:

{query}
""".strip()