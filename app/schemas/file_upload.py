from fastapi import BaseModel
from datetime import datetime


class OCRResponse(BaseModel):
    job_id: str
    filename: str
    extracted_text: str
    status: str = "completed"
    processed_at: datetime


class ErrorResponse(BaseModel):
    detail: str
