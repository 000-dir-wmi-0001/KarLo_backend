"""create_user_table

Revision ID: 5effd0129519
Revises: 04889157e0eb
Create Date: 2025-10-05 01:52:33.997879

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import enum


# revision identifiers, used by Alembic.
revision: str = '5effd0129519'
down_revision: Union[str, Sequence[str], None] = '04889157e0eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# --- Enum definition for roles ---
class UserRole(enum.Enum):
    ADMIN = "admin"
    TECHNICIAN = "technician"
    USER = "user"


def upgrade() -> None:
    """Upgrade schema."""
    # Create the Postgres enum type only if it doesn't exist to avoid duplicate-type errors.
    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'userrole') THEN
                CREATE TYPE userrole AS ENUM ('admin','technician','user');
            END IF;
        END$$;
        """
    )

    # Use an explicit sa.Enum referencing the literal values so the column uses the
    # already-created Postgres enum. Set create_type=False so SQLAlchemy does not
    # attempt to create the type again during the table DDL (we already ensured
    # type exists above with a DO block).
    user_role_enum = sa.Enum('admin', 'technician', 'user', name="userrole", create_type=False)

    # Create table
    op.create_table(
        "home_cure_user",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("full_name", sa.String, index=True),
        sa.Column("phone_number", sa.String, index=True, nullable=True),
        sa.Column("email", sa.String, index=True, unique=True, nullable=False),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("gender", sa.String, index=True, nullable=True),
        sa.Column("date_of_birth", sa.DateTime, index=True, nullable=True),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("is_superuser", sa.Boolean, default=False),
        sa.Column("is_verified", sa.Boolean, default=True),
        sa.Column("is_deleted", sa.Boolean, default=False),

        sa.Column("profile_picture", sa.String, nullable=True),
        sa.Column("bio", sa.String, nullable=True),
        sa.Column("country", sa.String, index=True, nullable=True),
        sa.Column("state", sa.String, index=True, nullable=True),
        sa.Column("city", sa.String, index=True, nullable=True),
        sa.Column("zip_code", sa.String, index=True, nullable=True),
        sa.Column("address", sa.String, index=True, nullable=True),
        sa.Column("geo_location", sa.String, index=True, nullable=True),

    # Use STRING in migration to avoid creating Postgres enum during table DDL.
    # The application model can still map to an Enum at runtime; using string
    # here prevents duplicate-type creation errors during migrations.
    sa.Column("role", sa.String, nullable=False, server_default="user"),

        sa.Column("geo_location", sa.String, nullable=True),
        sa.Column("last_login", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("home_cure_user")
    sa.Enum(name="userrole").drop(op.get_bind(), checkfirst=True)
