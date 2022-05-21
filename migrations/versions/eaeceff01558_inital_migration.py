"""Inital migration

Revision ID: eaeceff01558
Revises: 
Create Date: 2022-05-18 18:07:15.039400

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eaeceff01558'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('User',
    sa.Column('username', sa.String(length=45), nullable=False),
    sa.Column('emailAdresse', sa.String(length=45), nullable=False),
    sa.Column('password', sa.String(length=45), nullable=False),
    sa.Column('rolle', sa.Integer(), nullable=False),
    sa.Column('isLoggedIn', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('username'),
    sa.UniqueConstraint('emailAdresse')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('User')
    # ### end Alembic commands ###