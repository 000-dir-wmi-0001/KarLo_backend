import pyotp
import qrcode
import io
import json
import secrets
import base64
from datetime import datetime, timezone


def generate_setup(user) -> dict:
    secret = pyotp.random_base32()
    uri = pyotp.TOTP(secret).provisioning_uri(name=user.email, issuer_name="KarLo")
    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    qr_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return {"secret": secret, "uri": uri, "qr_svg": f"data:image/png;base64,{qr_b64}"}


def verify_code(secret: str, code: str) -> bool:
    return pyotp.TOTP(secret).verify(code, valid_window=1)


def generate_backup_codes() -> list[str]:
    return [secrets.token_hex(4).upper() for _ in range(8)]


def enable_mfa(user, secret: str, code: str, db) -> list[str]:
    if not verify_code(secret, code):
        raise ValueError("Invalid code")
    backup_codes = generate_backup_codes()
    user.mfa_secret = secret
    user.mfa_enabled = True
    user.mfa_enabled_at = datetime.now(timezone.utc)
    user.mfa_backup_codes = json.dumps(backup_codes)
    db.commit()
    db.refresh(user)
    return backup_codes


def disable_mfa(user, db) -> None:
    user.mfa_enabled = False
    user.mfa_secret = None
    user.mfa_backup_codes = None
    user.mfa_enabled_at = None
    db.commit()


def verify_login(user, code: str) -> bool:
    if not user.mfa_enabled or not user.mfa_secret:
        return True
    # Check TOTP
    if verify_code(user.mfa_secret, code):
        return True
    # Check backup codes
    if user.mfa_backup_codes:
        codes: list[str] = json.loads(user.mfa_backup_codes)
        if code.upper() in codes:
            codes.remove(code.upper())
            user.mfa_backup_codes = json.dumps(codes)
            return True
    return False
