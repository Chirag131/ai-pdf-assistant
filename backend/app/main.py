from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="RAG AI BOT",
    version='0.1.0'
)

app.include_router(router)

@app.get('/health')
def health_check():
    return {
        "status": "ok",
        "message": "AI PDF Assistant API is running",
    }