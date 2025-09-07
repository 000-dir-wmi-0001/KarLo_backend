"""added new models

Revision ID: ac0e72eb2ff6
Revises: 491812872a08
Create Date: 2025-09-07 10:57:19.373119

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac0e72eb2ff6'
down_revision: Union[str, Sequence[str], None] = '491812872a08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """No-op: this migration previously dropped tables; it's now intentionally empty."""
    pass


def downgrade() -> None:
    """No-op."""
    pass
