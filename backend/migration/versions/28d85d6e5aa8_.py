"""empty message

Revision ID: 28d85d6e5aa8
Revises: 0b9a91ac7f48
Create Date: 2023-12-26 00:49:29.485649

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28d85d6e5aa8'
down_revision: Union[str, None] = '0b9a91ac7f48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('age_ratings', 'type',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('age_ratings', 'name',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('age_ratings', 'name',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('age_ratings', 'type',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    # ### end Alembic commands ###
