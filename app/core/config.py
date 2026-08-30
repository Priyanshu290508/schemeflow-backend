# SchemeFlow Core Configuration
import os
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "SchemeFlow"
    API_V1_STR: str = "/api"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./schemeflow.db")
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]
    # Default Rule Scoring Weights
    WEIGHT_AGE: float = 20.0
    WEIGHT_INCOME: float = 25.0
    WEIGHT_BUSINESS_TYPE: float = 25.0
    WEIGHT_LOCATION: float = 15.0
    WEIGHT_FINANCIAL_NEED: float = 15.0

settings = Settings()
