from fastapi import APIRouter, UploadFile, HTTPException, status, BackgroundTasks
from fastapi import File
from typing import Annotated
from app.schemas.file_upload import OCRResponse
from app.services.file_upload import FileService
import uuid
from datetime import datetime

router = APIRouter()


@router.post("/upload", response_model=OCRResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: Annotated[UploadFile, File(description="Image or PDF file for OCR")]
):
    if not file.filename:
        raise HTTPException(400, "No file selected")

    # Validate
    await FileService.validate_upload_file(file)

    job_id = str(uuid.uuid4())

    # Process (in production move to background task + Celery/RabbitMQ)
    extracted_text = await FileService.save_and_process(file, job_id)

    return OCRResponse(
        job_id=job_id,
        filename=file.filename,
        extracted_text=extracted_text,
        processed_at=datetime.utcnow(),
    )