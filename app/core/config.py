from dotenv import load_dotenv
import os

load_dotenv()

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

    # Password Hashing
    HASH_ALGORITHM: str = os.getenv("HASH_ALGORITHM", "bcrypt")
    HASH_ROUNDS: int = int(os.getenv("HASH_ROUNDS", 12))

    # Mail settings
    EMAIL: str = os.getenv("EMAIL")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    MAIL_USERNAME: str | None = os.getenv("MAIL_USERNAME") or os.getenv("EMAIL")
    MAIL_PASSWORD: str | None = os.getenv("MAIL_PASSWORD") or os.getenv("EMAIL_PASSWORD")
    MAIL_FROM: str | None = os.getenv("MAIL_FROM") or os.getenv("EMAIL")
    MAIL_FROM_NAME: str | None = os.getenv("MAIL_FROM_NAME")
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", 587))
    MAIL_STARTTLS: bool = os.getenv("MAIL_STARTTLS", "true").lower() == "true"
    MAIL_SSL_TLS: bool = os.getenv("MAIL_SSL_TLS", "false").lower() == "true"
    MAIL_USE_CREDENTIALS: bool = os.getenv("MAIL_USE_CREDENTIALS", "true").lower() == "true"
    MAIL_VALIDATE_CERTS: bool = os.getenv("MAIL_VALIDATE_CERTS", "true").lower() == "true"
    MAIL_SUPPRESS_SEND: bool = os.getenv("MAIL_SUPPRESS_SEND", "false").lower() == "true"
    MAIL_TEMPLATE_FOLDER: str | None = os.getenv("MAIL_TEMPLATE_FOLDER")
    EMAIL_ADMIN: str = os.getenv("EMAIL_ADMIN", "admin@example.com")
    ORIGIN_URL: str = os.getenv("ORIGIN_URL")

    # Environment
    ENV: str = os.getenv("ENV", "development")


settings = Settings()
