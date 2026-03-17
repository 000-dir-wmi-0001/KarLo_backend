"""
Seed script — creates or updates the superadmin account.
Run from the KarLo_backend directory:
    python scripts/seed_superadmin.py
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.karlo_c.models.user_model import KarloUser
from app.utils.security import hash_password

# ── Superadmin credentials ─────────────────────────────────────────────────
SUPERADMIN_EMAIL    = "admin@karlo.com"
SUPERADMIN_PASSWORD = "Admin@1234"
SUPERADMIN_NAME     = "Super Admin"
# ──────────────────────────────────────────────────────────────────────────

def seed():
    db = SessionLocal()
    try:
        existing = db.query(KarloUser).filter(KarloUser.email == SUPERADMIN_EMAIL).first()

        if existing:
            existing.full_name     = SUPERADMIN_NAME
            existing.hashed_password = hash_password(SUPERADMIN_PASSWORD)
            existing.is_superuser  = True
            existing.is_active     = True
            existing.is_verified   = True
            existing.role          = "admin"
            existing.agreed_to_terms = True
            db.commit()
            print(f"[✓] Superadmin updated: {SUPERADMIN_EMAIL}")
        else:
            user = KarloUser(
                full_name        = SUPERADMIN_NAME,
                email            = SUPERADMIN_EMAIL,
                hashed_password  = hash_password(SUPERADMIN_PASSWORD),
                is_superuser     = True,
                is_active        = True,
                is_verified      = True,
                role             = "admin",
                agreed_to_terms  = True,
                newsletter_opt_in = False,
            )
            db.add(user)
            db.commit()
            print(f"[✓] Superadmin created: {SUPERADMIN_EMAIL}")

        print(f"    Email    : {SUPERADMIN_EMAIL}")
        print(f"    Password : {SUPERADMIN_PASSWORD}")

    except Exception as e:
        db.rollback()
        print(f"[✗] Failed: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    seed()
