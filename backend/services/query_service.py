from services.llm_service import client


def normalize_query(query: str) -> str:
    """
    Correct obvious spelling and grammar mistakes in a search query
    without changing its meaning.
    """

    cleaned_query = query.strip()

    if not cleaned_query:
        raise ValueError("Query cannot be empty.")

    prompt = f"""
Correct only obvious spelling and grammar mistakes in the following
search query.

Rules:
- Preserve the original meaning.
- Do not answer the question.
- Do not add new information.
- Do not explain your changes.
- Preserve names and technical terms unless there is an obvious typo.
- Return only the corrected query.

Query:
{cleaned_query}
"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
    )

    if not response.text:
        return cleaned_query

    return response.text.strip()