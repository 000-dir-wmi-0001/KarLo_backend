from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DATABASE: str = os.getenv("DATABASE")
    DB_USER: str = os.getenv("DB_USER")

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # Convert comma-separated string to list
    CORS_ORIGINS: list[str] = os.getenv("CORS_ORIGINS", "").split(",")

    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"


settings = Settings()
