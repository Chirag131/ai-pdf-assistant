import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "API Key missing."
    )

client = genai.Client(api_key=API_KEY)

def generate_answer(prompt:str) -> str:
    if not prompt.strip():
        raise ValueError("Prompt cannot be empty")

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
    )
    
    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return response.text