"""Update: Payroll model

Revision ID: 86afa957096e
Revises: 0a46b7961332
Create Date: 2025-05-10 12:28:04.964201

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86afa957096e'
down_revision: Union[str, None] = '0a46b7961332'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'payrolls', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'payrolls', type_='unique')
    # ### end Alembic commands ###
