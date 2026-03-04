from fastapi import UploadFile, HTTPException
import aiofiles
from app.core.config import settings


class FileService:

    @staticmethod
    def mock_ocr_processing(filename: str) -> str:
        """Replace this with real OCR (Tesseract, EasyOCR, PaddleOCR, or cloud API)."""
        return (
            f"[MOCK OCR RESULT]\n"
            f"Document: {filename}\n"
            f"Extracted text would appear here...\n"
            f"• Page 1: Lorem ipsum dolor sit amet...\n"
            f"• Detected language: en\n"
            f"Confidence: 0.92 (placeholder)"
        )

    @staticmethod
    async def save_and_process(file: UploadFile, job_id: str) -> str:
        """Stream file to disk (best practice for any size) and run placeholder OCR."""
        file_path = settings.UPLOAD_DIR / f"{job_id}_{file.filename}"

        # Stream write (memory efficient)
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(1024 * 1024):  # 1MB chunks
                await f.write(chunk)

        # Simulate OCR (in real life this would be background task + queue)
        extracted = FileService.mock_ocr_processing(file.filename)
        return extracted

    @staticmethod
    async def validate_upload_file(file: UploadFile):
        if file.content_type not in settings.ALLOWED_CONTENT_TYPES:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Invalid file type '{file.content_type}'."
                    f"Allowed: {settings.ALLOWED_CONTENT_TYPES}"
                )
            )

        # Check size (must read to know exact size — UploadFile.size is optional)
        contents = await file.read()
        if len(contents) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=(
                    "File too large. Max allowed:"
                    f"{settings.MAX_FILE_SIZE // (1024*1024)}MB"
                )
            )
        await file.seek(0)  # Reset for later streaming
        return contents
