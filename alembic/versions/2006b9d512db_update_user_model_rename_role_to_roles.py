"""Update: User model - rename role to roles

Revision ID: 2006b9d512db
Revises: 5df2e8395f7c
Create Date: 2025-05-03 12:18:23.410636

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2006b9d512db'
down_revision: Union[str, None] = '5df2e8395f7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_supervisors',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('role', sa.String(length=50), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=True),
    sa.Column('supervisor_id', sa.Uuid(), nullable=True),
    sa.ForeignKeyConstraint(['supervisor_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_supervisors_role'), 'user_supervisors', ['role'], unique=True)
    op.create_unique_constraint(None, 'departments', ['name'])
    op.create_unique_constraint(None, 'leave_types', ['name'])
    op.drop_constraint('users_role_id_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'role_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role_id', sa.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key('users_role_id_fkey', 'users', 'roles', ['role_id'], ['id'])
    op.drop_constraint(None, 'leave_types', type_='unique')
    op.drop_constraint(None, 'departments', type_='unique')
    op.drop_index(op.f('ix_user_supervisors_role'), table_name='user_supervisors')
    op.drop_table('user_supervisors')
    # ### end Alembic commands ###
