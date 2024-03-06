"""transactions

Revision ID: 27a780b5cc1b
Revises: 2a451727e6a1
Create Date: 2024-03-06 12:43:27.688854

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27a780b5cc1b'
down_revision = '2a451727e6a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_username', sa.String(length=64), nullable=False),
    sa.Column('receiver_username', sa.String(length=64), nullable=False),
    sa.Column('amount', sa.String(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['sender_username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction')
    # ### end Alembic commands ###