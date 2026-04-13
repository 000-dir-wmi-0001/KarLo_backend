"""merge_all_heads

Revision ID: 7bbe4ac6362a
Revises: a1b8279de057, d3e4f5a6b7c8, d4e5f6a7b8c9
Create Date: 2026-04-13 19:49:51.729408

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7bbe4ac6362a'
down_revision: Union[str, Sequence[str], None] = ('a1b8279de057', 'd3e4f5a6b7c8', 'd4e5f6a7b8c9')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
