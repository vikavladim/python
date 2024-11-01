"""empty message

Revision ID: 24228b5af384
Revises: 
Create Date: 2024-10-08 15:22:06.955500

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '24228b5af384'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('officers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('rank', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('first_name', 'last_name', 'rank')
    )
    op.create_table('spaceships',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('alignment', sa.Enum('Ally', 'Enemy', name='alignment'), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('ship_class', sa.String(), nullable=True),
    sa.Column('length', sa.Float(), nullable=True),
    sa.Column('crew_size', sa.Integer(), nullable=True),
    sa.Column('is_armed', sa.Boolean(), nullable=True),
    sa.Column('speed', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ship_officers',
    sa.Column('ship_id', sa.Integer(), nullable=True),
    sa.Column('officer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['officer_id'], ['officers.id'], ),
    sa.ForeignKeyConstraint(['ship_id'], ['spaceships.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ship_officers')
    op.drop_table('spaceships')
    op.drop_table('officers')
    # ### end Alembic commands ###
