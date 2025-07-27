"""add fk,owner id in post & users tabel 

Revision ID: ac2a5162df76
Revises: 7d7c44edf04c
Create Date: 2025-07-21 20:15:01.476728

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac2a5162df76'
down_revision: Union[str, None] = '7d7c44edf04c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer,nullable=False))
    op.create_foreign_key('post_users_fk', 'posts', 'users', ['owner_id'], ['id'], 
    ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk',table_name="posts")
    op.drop_column('posts','owner_id')
    pass
