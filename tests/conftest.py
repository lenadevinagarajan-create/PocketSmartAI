import os
os.environ["DATABASE_URL"] = "sqlite:///./test_pocketsmart.db"
os.environ["GEMINI_API_KEY"] = ""
from app.main import app
