"""merging JavaScriptChallenge and CSharpChallenge migrations

Revision ID: d6c9367fa8a8
Revises: d33907401bd4, 5d1b887ff54f
Create Date: 2021-10-09 11:47:32.917582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6c9367fa8a8'
down_revision = ('d33907401bd4', '5d1b887ff54f')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
