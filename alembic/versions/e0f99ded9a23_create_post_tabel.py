"""create post tabel

Revision ID: e0f99ded9a23
Revises: 
Create Date: 2025-07-19 16:26:00.272774

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0f99ded9a23'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',
                     sa.Column('id',sa.Integer,nullable=False,primary_key=True),
                     sa.Column('title',sa.String,nullable=False),
                     sa.Column('content',sa.String,nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
