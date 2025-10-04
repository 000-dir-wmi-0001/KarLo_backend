"""create home_cure contact table

Revision ID: 4767e7001565
Revises: 1d2e083ac864
Create Date: 2025-10-04 18:20:28.730463
"""

from alembic import op
import sqlalchemy as sa

# --- Alembic revision identifiers ---
revision: str = '4767e7001565'
down_revision: str = '1d2e083ac864'
branch_labels: str = None
depends_on: str = None

# --- Migration functions ---
def upgrade():
    op.create_table(
        'home_cure_contact',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(), index=True, nullable=False),
        sa.Column('email', sa.String(), index=True, nullable=False),
        sa.Column('phone', sa.String(length=10), index=True, nullable=True),
        sa.Column('message', sa.String(), nullable=True),
    )

def downgrade():
    op.drop_table('home_cure_contact')
