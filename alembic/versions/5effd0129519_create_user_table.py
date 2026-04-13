"""create_user_table

Revision ID: 5effd0129519
Revises: 04889157e0eb
Create Date: 2025-10-05 01:52:33.997879

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import enum


# revision identifiers, used by Alembic.
revision: str = '5effd0129519'
down_revision: Union[str, Sequence[str], None] = '04889157e0eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# --- Enum definition for roles ---
class UserRole(enum.Enum):
    ADMIN = "admin"
    TECHNICIAN = "technician"
    USER = "user"


def upgrade() -> None:
    pass  # stale migration from old project, no-op

def downgrade() -> None:
    pass
