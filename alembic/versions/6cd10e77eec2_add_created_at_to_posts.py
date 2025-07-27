"""add_created_at_to_posts

Revision ID: 6cd10e77eec2
Revises: 7a7754de980f
Create Date: 2025-07-27 16:06:12.899082

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6cd10e77eec2'
down_revision: Union[str, None] = '7a7754de980f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','created_at')
    pass
