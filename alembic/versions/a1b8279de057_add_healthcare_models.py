"""add healthcare models

Revision ID: a1b8279de057
Revises: 5effd0129519
Create Date: 2025-10-12 12:04:47.888335

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b8279de057'
down_revision: Union[str, Sequence[str], None] = '5effd0129519'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Add healthcare models."""
    
    # Create Technician table
    op.create_table(
        'home_cure_technician',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('specialization', sa.String(length=255), nullable=False),
        sa.Column('certifications', sa.JSON(), nullable=True),
        sa.Column('experience_years', sa.Integer(), nullable=True),
        sa.Column('license_number', sa.String(length=100), nullable=True),
        sa.Column('rating', sa.Float(), nullable=True),
        sa.Column('total_reviews', sa.Integer(), nullable=True),
        sa.Column('completed_bookings', sa.Integer(), nullable=True),
        sa.Column('is_available', sa.Boolean(), nullable=True),
        sa.Column('availability_schedule', sa.JSON(), nullable=True),
        sa.Column('service_areas', sa.JSON(), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('profile_picture', sa.String(length=500), nullable=True),
        sa.Column('is_verified', sa.Boolean(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['home_cure_user.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('license_number'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_home_cure_technician_id'), 'home_cure_technician', ['id'], unique=False)
    
    # Create Booking table
    op.create_table(
        'home_cure_booking',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('technician_id', sa.Integer(), nullable=True),
        sa.Column('service_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('scheduled_date', sa.String(length=100), nullable=False),
        sa.Column('scheduled_time', sa.String(length=50), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), nullable=True),
        sa.Column('service_address', sa.Text(), nullable=False),
        sa.Column('service_location', sa.String(length=255), nullable=True),
        sa.Column('qr_code', sa.Text(), nullable=True),
        sa.Column('qr_code_data', sa.String(length=500), nullable=True),
        sa.Column('total_amount', sa.Float(), nullable=False),
        sa.Column('payment_status', sa.String(length=50), nullable=True),
        sa.Column('payment_method', sa.String(length=50), nullable=True),
        sa.Column('user_notes', sa.Text(), nullable=True),
        sa.Column('technician_notes', sa.Text(), nullable=True),
        sa.Column('admin_notes', sa.Text(), nullable=True),
        sa.Column('user_rating', sa.Float(), nullable=True),
        sa.Column('user_review', sa.Text(), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.Column('completed_at', sa.String(), nullable=True),
        sa.Column('cancelled_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['service_id'], ['home_cure_service.id'], ),
        sa.ForeignKeyConstraint(['technician_id'], ['home_cure_technician.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['home_cure_user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_home_cure_booking_id'), 'home_cure_booking', ['id'], unique=False)
    
    # Create Health Record table
    op.create_table(
        'home_cure_health_record',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('booking_id', sa.Integer(), nullable=True),
        sa.Column('record_type', sa.String(length=100), nullable=False),
        sa.Column('record_date', sa.String(length=100), nullable=False),
        sa.Column('diagnosis', sa.Text(), nullable=True),
        sa.Column('treatment', sa.Text(), nullable=True),
        sa.Column('medications', sa.JSON(), nullable=True),
        sa.Column('vitals', sa.JSON(), nullable=True),
        sa.Column('documents', sa.JSON(), nullable=True),
        sa.Column('lab_results', sa.JSON(), nullable=True),
        sa.Column('provider_name', sa.String(length=255), nullable=True),
        sa.Column('provider_notes', sa.Text(), nullable=True),
        sa.Column('follow_up_required', sa.String(length=10), nullable=True),
        sa.Column('follow_up_date', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['booking_id'], ['home_cure_booking.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['home_cure_user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_home_cure_health_record_id'), 'home_cure_health_record', ['id'], unique=False)
    
    # Create Technician Earnings table
    op.create_table(
        'home_cure_technician_earnings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('technician_id', sa.Integer(), nullable=False),
        sa.Column('booking_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('commission_rate', sa.Float(), nullable=True),
        sa.Column('net_earnings', sa.Float(), nullable=False),
        sa.Column('payment_status', sa.String(length=50), nullable=True),
        sa.Column('payment_date', sa.String(length=100), nullable=True),
        sa.Column('payment_method', sa.String(length=100), nullable=True),
        sa.Column('transaction_id', sa.String(length=255), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['booking_id'], ['home_cure_booking.id'], ),
        sa.ForeignKeyConstraint(['technician_id'], ['home_cure_technician.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_home_cure_technician_earnings_id'), 'home_cure_technician_earnings', ['id'], unique=False)
    
    # Create Admin Log table
    op.create_table(
        'home_cure_admin_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('admin_user_id', sa.Integer(), nullable=False),
        sa.Column('action', sa.String(length=255), nullable=False),
        sa.Column('entity_type', sa.String(length=100), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('previous_values', sa.JSON(), nullable=True),
        sa.Column('new_values', sa.JSON(), nullable=True),
        sa.Column('ip_address', sa.String(length=50), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['admin_user_id'], ['home_cure_user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_home_cure_admin_log_id'), 'home_cure_admin_log', ['id'], unique=False)
    
    # Create System Settings table
    op.create_table(
        'home_cure_system_settings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('key', sa.String(length=255), nullable=False),
        sa.Column('value', sa.Text(), nullable=False),
        sa.Column('data_type', sa.String(length=50), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_editable', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.Column('updated_at', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('key')
    )
    op.create_index(op.f('ix_home_cure_system_settings_id'), 'home_cure_system_settings', ['id'], unique=False)
    op.create_index(op.f('ix_home_cure_system_settings_key'), 'home_cure_system_settings', ['key'], unique=True)
    
    # Create Notification table
    op.create_table(
        'home_cure_notification',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('notification_type', sa.String(length=100), nullable=False),
        sa.Column('related_entity_type', sa.String(length=100), nullable=True),
        sa.Column('related_entity_id', sa.Integer(), nullable=True),
        sa.Column('is_read', sa.Boolean(), nullable=True),
        sa.Column('read_at', sa.String(), nullable=True),
        sa.Column('priority', sa.String(length=50), nullable=True),
        sa.Column('action_url', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['home_cure_user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_home_cure_notification_id'), 'home_cure_notification', ['id'], unique=False)
    
    # Update Service table with new columns
    op.add_column('home_cure_service', sa.Column('duration_minutes', sa.Integer(), nullable=True))
    op.add_column('home_cure_service', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.add_column('home_cure_service', sa.Column('category', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema - Remove healthcare models."""
    
    # Remove columns from Service table
    op.drop_column('home_cure_service', 'category')
    op.drop_column('home_cure_service', 'is_active')
    op.drop_column('home_cure_service', 'duration_minutes')
    
    # Drop tables in reverse order
    op.drop_index(op.f('ix_home_cure_notification_id'), table_name='home_cure_notification')
    op.drop_table('home_cure_notification')
    
    op.drop_index(op.f('ix_home_cure_system_settings_key'), table_name='home_cure_system_settings')
    op.drop_index(op.f('ix_home_cure_system_settings_id'), table_name='home_cure_system_settings')
    op.drop_table('home_cure_system_settings')
    
    op.drop_index(op.f('ix_home_cure_admin_log_id'), table_name='home_cure_admin_log')
    op.drop_table('home_cure_admin_log')
    
    op.drop_index(op.f('ix_home_cure_technician_earnings_id'), table_name='home_cure_technician_earnings')
    op.drop_table('home_cure_technician_earnings')
    
    op.drop_index(op.f('ix_home_cure_health_record_id'), table_name='home_cure_health_record')
    op.drop_table('home_cure_health_record')
    
    op.drop_index(op.f('ix_home_cure_booking_id'), table_name='home_cure_booking')
    op.drop_table('home_cure_booking')
    
    op.drop_index(op.f('ix_home_cure_technician_id'), table_name='home_cure_technician')
    op.drop_table('home_cure_technician')
