import os
from pathlib import Path
from dotenv import load_dotenv
from typing import List

# Load .env từ folder gốc project
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Config:
    # LLM Configuration
    LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "http://localhost:8000/v1")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-2.5-flash-lite")
    # Google Sheets
    GOOGLE_SHEET_ID: str = os.getenv("GOOGLE_SHEET_ID")
    CREDENTIALS_PATH: str = os.getenv("CREDENTIALS_PATH", "config/crdt.json")
    # Zalo Bot
    ZALO_TOKEN: str = os.getenv("ZALO_TOKEN")
    WEBHOOK_URL: str = os.getenv("WEBHOOK_URL")
    # Validation
    @staticmethod
    def validate():
        #check env vars
        required = ["LLM_BASE_URL", "ZALO_TOKEN", "WEBHOOK_URL"]
        missing = [key for key in required if not os.getenv(key)]
        if missing:
            raise ValueError(f"Missing env vars: {', '.join(missing)}")
        #check file credentials.json
        creds_path = Config.CREDENTIALS_PATH 
        if not os.path.exists(creds_path):
            raise FileNotFoundError(f"Credentials file not found: {creds_path}")