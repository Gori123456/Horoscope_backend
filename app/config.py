import os
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "Deterministic Horoscope API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Database URL: Supports PostgreSQL. Defaults to local SQLite if POSTGRES_URL not provided
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        os.getenv("POSTGRES_URL", "sqlite:///./horoscope.db")
    )
    
    # CORS Origins
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "*"
    ]
    
    # Default Ayanamsha (Lahiri / Chitra Paksha)
    DEFAULT_AYANAMSHA: str = "Lahiri"

settings = Settings()

