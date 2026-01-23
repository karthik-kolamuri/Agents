import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Agno / LLM
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # Google Workspace
    GOOGLE_APPLICATION_CREDENTIALS: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "google_credentials.json")
    GOOGLE_SHEET_ID: str = os.getenv("GOOGLE_SHEET_ID", "")
    
    # Twilio / WhatsApp
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_FROM_NUMBER: str = os.getenv("TWILIO_FROM_NUMBER", "whatsapp:+14155238886")
    
    # Email Configuration
    STAFF_EMAIL: str = os.getenv("STAFF_EMAIL", "karthik.kolamuri@sasi.ac.in")

    # Feature Flags
    MOCK_MODE: bool = True # Set to False to use real APIs

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:Ka45h8k%40@localhost:5433/legal_intake_db")

settings = Settings()
