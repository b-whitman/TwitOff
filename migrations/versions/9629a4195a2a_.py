"""empty message

Revision ID: 9629a4195a2a
Revises: eb074bf6328c
Create Date: 2020-02-21 18:06:57.070957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9629a4195a2a'
down_revision = 'eb074bf6328c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('screen_name', sa.String(length=128), nullable=True),
    sa.Column('followers_count', sa.Integer(), nullable=True),
    sa.Column('latest_tweet_id', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tweet',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('full_text', sa.String(length=500), nullable=True),
    sa.Column('embedding', sa.PickleType(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tweet')
    op.drop_table('user')
    # ### end Alembic commands ###
