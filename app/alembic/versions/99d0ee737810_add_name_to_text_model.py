"""add name to text model

Revision ID: 99d0ee737810
Revises: 67ebf262ad8c
Create Date: 2024-01-22 00:05:54.920538

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99d0ee737810'
down_revision = '67ebf262ad8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('text', sa.Column('name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('text', 'name')
    # ### end Alembic commands ###
