"""added column into table 'user'

Revision ID: 58612e0933d8
Revises: 050d9284edef
Create Date: 2023-04-11 23:24:02.611257

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58612e0933d8'
down_revision = '050d9284edef'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('hashed_password', sa.String(), nullable=False))
    op.add_column('user', sa.Column('is_active', sa.Boolean(), nullable=False))
    op.add_column('user', sa.Column('is_superuser', sa.Boolean(), nullable=False))
    op.add_column('user', sa.Column('is_verified', sa.Boolean(), nullable=False))
    op.drop_column('user', 'password')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('user', 'is_verified')
    op.drop_column('user', 'is_superuser')
    op.drop_column('user', 'is_active')
    op.drop_column('user', 'hashed_password')
    # ### end Alembic commands ###
