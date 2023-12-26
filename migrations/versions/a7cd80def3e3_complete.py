"""Complete

Revision ID: a7cd80def3e3
Revises: ac3b99794216
Create Date: 2023-04-06 02:25:39.453931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7cd80def3e3'
down_revision = 'ac3b99794216'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('New Employees', sa.Column('phone_number', sa.String(), nullable=True))
    op.drop_column('New Employees', 'phn_number')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('New Employees', sa.Column('phn_number', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('New Employees', 'phone_number')
    # ### end Alembic commands ###
