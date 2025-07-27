"""add user tabel

Revision ID: 7d7c44edf04c
Revises: 193cd446f247
Create Date: 2025-07-21 17:35:19.322539

"""
from cgitb import text
from time import timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d7c44edf04c'
down_revision: Union[str, None] = '193cd446f247'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id',sa.Integer,nullable=False,primary_key=True),
                    sa.Column('email',sa.String,nullable=False,unique=True),
                    sa.Column('password',sa.String,nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,
                               server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
