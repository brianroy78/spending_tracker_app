"""first migration

Revision ID: 434f52681970
Revises: 
Create Date: 2023-05-25 10:16:12.139236

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '434f52681970'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('keywords', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('note', sa.String(length=128), nullable=False),
    sa.Column('amount', sa.Numeric(precision=2), nullable=False),
    sa.Column('is_entry', sa.Boolean(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=False),
    sa.Column('method', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction')
    op.drop_table('category')
    # ### end Alembic commands ###