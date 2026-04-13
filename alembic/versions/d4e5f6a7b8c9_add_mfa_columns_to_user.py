"""add mfa columns to user

Revision ID: d4e5f6a7b8c9
Revises: c2d3e4f5a6b7
Create Date: 2025-01-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = 'd4e5f6a7b8c9'
down_revision = 'c2d3e4f5a6b7'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user') as batch_op:
        batch_op.add_column(sa.Column('mfa_enabled', sa.Boolean(), nullable=True, server_default='0'))
        batch_op.add_column(sa.Column('mfa_secret', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('mfa_backup_codes', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('mfa_enabled_at', sa.DateTime(timezone=True), nullable=True))


def downgrade():
    with op.batch_alter_table('user') as batch_op:
        batch_op.drop_column('mfa_enabled_at')
        batch_op.drop_column('mfa_backup_codes')
        batch_op.drop_column('mfa_secret')
        batch_op.drop_column('mfa_enabled')
