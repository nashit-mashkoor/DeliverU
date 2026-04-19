"""Introduce role-based users and remove is_superuser.

Revision ID: 20260419_0001
Revises:
Create Date: 2026-04-19 00:00:00.000000
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260419_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "user",
        sa.Column("role", sa.String(length=20), server_default="customer", nullable=True),
    )

    op.execute("UPDATE \"user\" SET role = 'admin' WHERE is_superuser = true")
    op.execute("UPDATE \"user\" SET role = 'customer' WHERE role IS NULL")

    op.alter_column("user", "role", existing_type=sa.String(length=20), nullable=False)
    op.create_check_constraint("ck_user_role_valid", "user", "role IN ('admin', 'customer', 'driver')")
    op.drop_column("user", "is_superuser")


def downgrade() -> None:
    op.add_column("user", sa.Column("is_superuser", sa.Boolean(), server_default=sa.false(), nullable=True))

    op.execute("UPDATE \"user\" SET is_superuser = true WHERE role = 'admin'")
    op.execute("UPDATE \"user\" SET is_superuser = false WHERE is_superuser IS NULL")

    op.alter_column("user", "is_superuser", existing_type=sa.Boolean(), nullable=False)
    op.drop_constraint("ck_user_role_valid", "user", type_="check")
    op.drop_column("user", "role")
