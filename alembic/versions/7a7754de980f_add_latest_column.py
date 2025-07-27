"""add latest column

Revision ID: 7a7754de980f
Revises: ac2a5162df76
Create Date: 2025-07-27 15:07:04.377592

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a7754de980f'
down_revision: Union[str, None] = 'ac2a5162df76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
