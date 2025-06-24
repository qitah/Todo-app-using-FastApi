"""add is_expired to task model

Revision ID: 0a1db8570f62
Revises: 
Create Date: 2025-06-24 14:19:38.004376

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0a1db8570f62'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add the is_expired column to the task table
    op.add_column('task', sa.Column('is_expired', sa.Boolean(), nullable=False, server_default=sa.false()))

def downgrade() -> None:
    """Downgrade schema."""
    # Remove the is_expired column from the task table
    op.drop_column('task', 'is_expired')
