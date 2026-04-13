"""create home_cure_user table

Revision ID: 04889157e0eb
Revises: 4767e7001565
Create Date: 2025-10-04 23:31:42.532269

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import enum
import sqlalchemy as _sa


# revision identifiers, used by Alembic.
revision: str = '04889157e0eb'
down_revision: Union[str, Sequence[str], None] = '4767e7001565'
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
