"""remove text url

Revision ID: 1d0defd3744e
Revises: 6e8d60461d89
Create Date: 2024-03-07 00:29:44.182465

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d0defd3744e'
down_revision = '6e8d60461d89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('text', 'url')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('text', sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
