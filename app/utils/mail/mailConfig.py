from fastapi_mail import ConnectionConfig
from app.core.config import settings
from pathlib import Path
import os

# Resolve the template folder path and ensure it exists to satisfy ConnectionConfig validation
default_templates_dir = Path(__file__).parent / "templates"
templates_dir = (
    Path(settings.MAIL_TEMPLATE_FOLDER).resolve()
    if settings.MAIL_TEMPLATE_FOLDER
    else default_templates_dir.resolve()
)
# Create directory if missing (no-op if it already exists)
templates_dir.mkdir(parents=True, exist_ok=True)

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM or settings.MAIL_USERNAME,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.MAIL_USE_CREDENTIALS,
    VALIDATE_CERTS=settings.MAIL_VALIDATE_CERTS,
    SUPPRESS_SEND=settings.MAIL_SUPPRESS_SEND,
    TEMPLATE_FOLDER=str(templates_dir),
)
