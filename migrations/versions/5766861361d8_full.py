"""full

Revision ID: 5766861361d8
Revises: 2d6440e769ba
Create Date: 2023-04-04 19:12:58.481329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5766861361d8'
down_revision = '2d6440e769ba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Employees', sa.Column('role', sa.String(), nullable=True))
    op.add_column('New Employees', sa.Column('role', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('New Employees', 'role')
    op.drop_column('Employees', 'role')
    # ### end Alembic commands ###
