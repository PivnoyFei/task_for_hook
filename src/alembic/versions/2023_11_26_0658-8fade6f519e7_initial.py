"""Initial

Revision ID: 8fade6f519e7
Revises: 
Create Date: 2023-11-26 06:58:43.579476

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8fade6f519e7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('round',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number_rounds', sa.Integer(), nullable=True),
    sa.Column('numbers_weight', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rounds_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number_rounds', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('cell', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('password', sa.LargeBinary(), nullable=False),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('auth_token',
    sa.Column('key', sa.String(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('key')
    )
    op.create_index(op.f('ix_auth_token_key'), 'auth_token', ['key'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_auth_token_key'), table_name='auth_token')
    op.drop_table('auth_token')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    op.drop_table('rounds_info')
    op.drop_table('round')
    # ### end Alembic commands ###