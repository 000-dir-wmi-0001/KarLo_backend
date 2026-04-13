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
    conn = op.get_bind()
    cols = [row[1] for row in conn.execute(sa.text("PRAGMA table_info(contact)"))]
    if 'name' not in cols:
        op.add_column('contact', sa.Column('name', sa.String(), nullable=True))
    indexes = [row[1] for row in conn.execute(sa.text("PRAGMA index_list(contact)"))]
    if 'ix_contact_name' not in indexes:
        op.create_index(op.f('ix_contact_name'), 'contact', ['name'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_contact_name'), table_name='contact')
    op.drop_column('contact', 'name')
