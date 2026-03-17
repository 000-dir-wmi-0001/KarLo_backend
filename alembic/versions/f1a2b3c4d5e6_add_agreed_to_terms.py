"""add agreed_to_terms and newsletter_opt_in to user

Revision ID: f1a2b3c4d5e6
Revises: ac0e72eb2ff6
Create Date: 2025-01-01 00:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'f1a2b3c4d5e6'
down_revision: Union[str, Sequence[str], None] = 'ac0e72eb2ff6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user', sa.Column('agreed_to_terms', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('user', sa.Column('newsletter_opt_in', sa.Boolean(), nullable=False, server_default=sa.false()))


def downgrade() -> None:
    op.drop_column('user', 'newsletter_opt_in')
    op.drop_column('user', 'agreed_to_terms')
