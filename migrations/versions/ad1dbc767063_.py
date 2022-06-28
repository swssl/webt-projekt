"""empty message

Revision ID: ad1dbc767063
Revises: d860e5a67f45
Create Date: 2022-06-26 15:32:48.456826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad1dbc767063'
down_revision = 'd860e5a67f45'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('HighlightInRoute')

    # not possible to add a constraint to an existing table in SQLite...
    # op.create_foreign_key('fk_Highlight_Route', 'Highlight', 'Route', ['routeId'], ['id'])

    # drop table and recreate with added foreign-key-constraint
    op.drop_table('Highlight')
    op.create_table('Highlight',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=45), nullable=False),
        sa.Column('description', sa.String(length=1024), nullable=True),
        sa.Column('previewImage', sa.String(length=255), nullable=False),
        sa.Column('latitude', sa.String(length=15), nullable=False),
        sa.Column('longitude', sa.String(length=15), nullable=False),
        sa.Column('creator', sa.String(length=45), nullable=True),
        sa.Column('routeId', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['creator'], ['User.username'], ),
        sa.ForeignKeyConstraint(['routeId'], ['Route.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    


def downgrade():
    op.create_table('HighlightInRoute',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('routeId', sa.Integer(), nullable=True),
        sa.Column('highlightId', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['highlightId'], ['Highlight.id'], ),
        sa.ForeignKeyConstraint(['routeId'], ['Route.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.drop_table('Highlight')
    op.create_table('Highlight',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=45), nullable=False),
        sa.Column('description', sa.String(length=1024), nullable=True),
        sa.Column('previewImage', sa.String(length=255), nullable=False),
        sa.Column('latitude', sa.String(length=15), nullable=False),
        sa.Column('longitude', sa.String(length=15), nullable=False),
        sa.Column('creator', sa.String(length=45), nullable=True),
        sa.ForeignKeyConstraint(['creator'], ['User.username'], ),
        sa.PrimaryKeyConstraint('id')
    )
