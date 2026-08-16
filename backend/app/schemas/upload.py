from pydantic import BaseModel


class UploadResponse(BaseModel):
    filename: str
    pages_extracted: int
    chunks_created: int