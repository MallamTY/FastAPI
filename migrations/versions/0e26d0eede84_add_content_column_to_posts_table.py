"""add content column to posts table

Revision ID: 0e26d0eede84
Revises: d90ed7406a97
Create Date: 2026-07-12 22:29:13.067337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e26d0eede84'
down_revision: Union[str, Sequence[str], None] = 'd90ed7406a97'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
