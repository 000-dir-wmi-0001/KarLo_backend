"""Initial migration: create base tables

Revision ID: 491812872a08
Revises: 
Create Date: 2025-08-03 14:57:50.332527

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '491812872a08'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create initial tables for contribute and contact."""
    # Contribute table
    op.create_table(
        'contribute',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('gitHub_link', sa.String(), nullable=True),
        sa.Column('linkedIn_link', sa.String(), nullable=True),
        sa.Column('country', sa.String(), nullable=True),
        sa.Column('state', sa.String(), nullable=True),
        sa.Column('city', sa.String(), nullable=True),
        sa.Column('zip_code', sa.String(), nullable=True),
    )
    op.create_index(op.f('ix_contribute_id'), 'contribute', ['id'], unique=False)
    op.create_index(op.f('ix_contribute_first_name'), 'contribute', ['first_name'], unique=False)
    op.create_index(op.f('ix_contribute_last_name'), 'contribute', ['last_name'], unique=False)
    op.create_index(op.f('ix_contribute_email'), 'contribute', ['email'], unique=False)
    op.create_index(op.f('ix_contribute_gitHub_link'), 'contribute', ['gitHub_link'], unique=False)
    op.create_index(op.f('ix_contribute_linkedIn_link'), 'contribute', ['linkedIn_link'], unique=False)
    op.create_index(op.f('ix_contribute_country'), 'contribute', ['country'], unique=False)
    op.create_index(op.f('ix_contribute_state'), 'contribute', ['state'], unique=False)
    op.create_index(op.f('ix_contribute_city'), 'contribute', ['city'], unique=False)
    op.create_index(op.f('ix_contribute_zip_code'), 'contribute', ['zip_code'], unique=False)

    # Contact table
    op.create_table(
        'contact',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('subject', sa.String(), nullable=True),
        sa.Column('message', sa.String(), nullable=True),
        sa.Column('website', sa.String(), nullable=True),
    )
    op.create_index(op.f('ix_contact_id'), 'contact', ['id'], unique=False)
    op.create_index(op.f('ix_contact_name'), 'contact', ['name'], unique=False)
    op.create_index(op.f('ix_contact_email'), 'contact', ['email'], unique=False)
    op.create_index(op.f('ix_contact_subject'), 'contact', ['subject'], unique=False)
    op.create_index(op.f('ix_contact_message'), 'contact', ['message'], unique=False)
    op.create_index(op.f('ix_contact_website'), 'contact', ['website'], unique=False)


def downgrade() -> None:
    # Drop contact indexes and table
    op.drop_index(op.f('ix_contact_website'), table_name='contact')
    op.drop_index(op.f('ix_contact_message'), table_name='contact')
    op.drop_index(op.f('ix_contact_subject'), table_name='contact')
    op.drop_index(op.f('ix_contact_email'), table_name='contact')
    op.drop_index(op.f('ix_contact_name'), table_name='contact')
    op.drop_index(op.f('ix_contact_id'), table_name='contact')
    op.drop_table('contact')

    # Drop contribute indexes and table
    op.drop_index(op.f('ix_contribute_zip_code'), table_name='contribute')
    op.drop_index(op.f('ix_contribute_city'), table_name='contribute')
    op.drop_index(op.f('ix_contribute_country'), table_name='contribute')
    op.drop_index(op.f('ix_contribute_email'), table_name='contribute')
    op.drop_index(op.f('ix_contribute_first_name'), table_name='contribute')
    op.drop_index(op.f('ix_contribute_gitHub_link'), table_name='contribute')
    op.drop_index(op.f('ix_contribute_last_name'), table_name='contribute')
    op.drop_index(op.f('ix_contribute_linkedIn_link'), table_name='contribute')
    op.drop_index(op.f('ix_contribute_state'), table_name='contribute')
    op.drop_index(op.f('ix_contribute_id'), table_name='contribute')
    op.drop_table('contribute')
