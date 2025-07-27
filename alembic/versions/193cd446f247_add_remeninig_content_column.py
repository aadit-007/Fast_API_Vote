"""add remeninig content column

Revision ID: 193cd446f247
Revises: e0f99ded9a23
Create Date: 2025-07-21 17:10:57.842821

"""
from cgitb import text
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '193cd446f247'
down_revision: Union[str, None] = 'e0f99ded9a23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean, nullable=False, 
    server_default='TRUE'))
    op.add_column('posts',sa.Column(
        'created_at',sa.TIMESTAMP(timezone=True),nullable=False, 
        server_default=sa.text('now()')))
    pass

def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts','created_at')
    pass
