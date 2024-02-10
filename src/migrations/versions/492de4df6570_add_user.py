"""add user

Revision ID: 492de4df6570
Revises: 61b2ad6a2eb4
Create Date: 2024-02-10 07:36:13.784908

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '492de4df6570'
down_revision = '61b2ad6a2eb4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=250), nullable=False),
    sa.Column('password', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
