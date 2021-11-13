"""Prepare user for authentication

Revision ID: 1479c14ac6f7
Revises: ecceabba75ad
Create Date: 2021-11-10 02:13:41.488293

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1479c14ac6f7'
down_revision = 'ecceabba75ad'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('user')
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('user')
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

