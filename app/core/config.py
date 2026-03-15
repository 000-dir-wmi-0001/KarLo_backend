from dotenv import load_dotenv
import os

load_dotenv()


def _optional_env(name: str) -> str | None:
    value = os.getenv(name)
    return value if value else None

class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DATABASE: str = os.getenv("DATABASE")
    DB_USER: str = os.getenv("DB_USER")

    # Security / JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
    COOKIE_SECURE: bool = os.getenv("COOKIE_SECURE", "false").lower() == "true"
    COOKIE_SAMESITE: str = os.getenv("COOKIE_SAMESITE", "lax")
    COOKIE_DOMAIN: str | None = _optional_env("COOKIE_DOMAIN")

    # Password Hashing
    HASH_ALGORITHM: str = os.getenv("HASH_ALGORITHM", "bcrypt")
    HASH_ROUNDS: int = int(os.getenv("HASH_ROUNDS", 12))

    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ORIGIN_URL: str = os.getenv("ORIGIN_URL")

    # Environment
    ENV: str = os.getenv("ENV", "development")


settings = Settings()
