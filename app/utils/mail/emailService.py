from fastapi_mail import FastMail, MessageSchema, MessageType
from typing import Iterable, Optional
from app.utils.mail.mailConfig import conf

fm = FastMail(conf)

async def send_email(
    subject: str,
    recipients: list[str] | tuple[str, ...],
    body: str,
    subtype: str = "html",
    attachments: Optional[Iterable[str]] = None,
    cc: Optional[list[str]] = None,
    bcc: Optional[list[str]] = None,
):
    """Send an email with optional attachments/cc/bcc.

    Returns a dict with success flag and message for logging.
    """
    message = MessageSchema(
        subject=subject,
        recipients=list(recipients),
        body=body,
        subtype=subtype,  # 'html' or 'plain'
        cc=cc or [],
        bcc=bcc or [],
        attachments=list(attachments) if attachments else None,
    )
    try:
        await fm.send_message(message)
        return {"success": True, "message": "Email sent"}
    except Exception as e:
        return {"success": False, "message": str(e)}
