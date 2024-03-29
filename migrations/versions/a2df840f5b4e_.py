"""empty message

Revision ID: a2df840f5b4e
Revises: 788137f81a92
Create Date: 2022-03-18 11:48:16.243274

"""
from alembic import op
import sqlalchemy as sa

import os
environment = os.getenv("FLASK_ENV")
SCHEMA = os.environ.get("SCHEMA")


# revision identifiers, used by Alembic.
revision = 'a2df840f5b4e'
down_revision = '788137f81a92'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('gamer_id', sa.Integer(), nullable=False),
    sa.Column('review', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['gamer_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    if environment == "production":
        op.execute(f"ALTER TABLE reviews SET SCHEMA {SCHEMA};")


def downgrade():
    op.drop_table('reviews')
