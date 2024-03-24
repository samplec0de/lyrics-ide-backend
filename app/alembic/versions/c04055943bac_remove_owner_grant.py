"""remove owner grant

Revision ID: c04055943bac
Revises: 1170617d3960
Create Date: 2024-03-24 03:39:00.217542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c04055943bac'
down_revision = '1170617d3960'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project_grant', sa.Column('is_active', sa.Boolean(), nullable=False))
    op.create_index(op.f('ix_project_grant_is_active'), 'project_grant', ['is_active'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_project_grant_is_active'), table_name='project_grant')
    op.drop_column('project_grant', 'is_active')
    # ### end Alembic commands ###
