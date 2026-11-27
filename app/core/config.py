import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "SQLGenPro")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b"
)

DATABASE_URL = os.getenv("DATABASE_URL", "")


def validate_config():

    if not DATABASE_URL:
        raise ValueError(
            "DATABASE_URL is missing in .env"
        )

    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is missing in .env"
        )
