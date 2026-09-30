import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

class Settings:
    app_name = os.getenv("APP_NAME", "PocketSmart AI")
    secret_key = os.getenv("SECRET_KEY", "change-this-development-secret")
    gemini_api_key = os.getenv("GEMINI_API_KEY", "")
    gemini_model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    database_url = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'pocketsmart.db'}")
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "true").lower() == "true"
    token_expire_minutes = int(os.getenv("TOKEN_EXPIRE_MINUTES", "120"))
    max_upload_mb = int(os.getenv("MAX_UPLOAD_MB", "5"))
    allowed_origins = [
        x.strip() for x in os.getenv("ALLOWED_ORIGINS", "http://127.0.0.1:8000,http://localhost:8000").split(",")
        if x.strip()
    ]

settings = Settings()
