"""add name to contact

Revision ID: b1c2d3e4f5a6
Revises: ac0e72eb2ff6
Create Date: 2025-09-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1c2d3e4f5a6'
down_revision: Union[str, Sequence[str], None] = 'ac0e72eb2ff6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add 'name' column to 'contact' table if not exists
    op.add_column('contact', sa.Column('name', sa.String(), nullable=True))
    op.create_index(op.f('ix_contact_name'), 'contact', ['name'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_contact_name'), table_name='contact')
    op.drop_column('contact', 'name')
