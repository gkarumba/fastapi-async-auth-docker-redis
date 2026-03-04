import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Settings:

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "mysql+pymysql://app_user:app_password@localhost:3306/app_db"
    )
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)

    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    ALLOWED_CONTENT_TYPES = {
        "image/jpeg",
        "image/png",
        "image/jpg",
        "application/pdf",
    }
    # Create local upload folder (demo only)
    UPLOAD_DIR = Path("uploads")
    UPLOAD_DIR.mkdir(exist_ok=True)


settings = Settings()
