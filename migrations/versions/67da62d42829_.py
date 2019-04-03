"""empty message

Revision ID: 67da62d42829
Revises: 
Create Date: 2019-03-31 17:42:11.372545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67da62d42829'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('manage_access',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('access_name', sa.String(length=40), nullable=False),
    sa.Column('path', sa.String(length=40), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('level', sa.SmallInteger(), nullable=True),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('update_time', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_manage_access_create_time'), 'manage_access', ['create_time'], unique=False)
    op.create_index(op.f('ix_manage_access_level'), 'manage_access', ['level'], unique=False)
    op.create_index(op.f('ix_manage_access_parent_id'), 'manage_access', ['parent_id'], unique=False)
    op.create_index(op.f('ix_manage_access_path'), 'manage_access', ['path'], unique=False)
    op.create_index(op.f('ix_manage_access_update_time'), 'manage_access', ['update_time'], unique=False)
    op.create_table('manage_role',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('role_name', sa.String(length=40), nullable=False),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('update_time', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_manage_role_create_time'), 'manage_role', ['create_time'], unique=False)
    op.create_index(op.f('ix_manage_role_role_name'), 'manage_role', ['role_name'], unique=False)
    op.create_index(op.f('ix_manage_role_update_time'), 'manage_role', ['update_time'], unique=False)
    op.create_table('manage_user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('update_time', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_manage_user_create_time'), 'manage_user', ['create_time'], unique=False)
    op.create_index(op.f('ix_manage_user_update_time'), 'manage_user', ['update_time'], unique=False)
    op.create_index(op.f('ix_manage_user_username'), 'manage_user', ['username'], unique=False)
    op.create_table('manager_role_access',
    sa.Column('manage_access_id', sa.Integer(), nullable=False),
    sa.Column('manage_role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['manage_access_id'], ['manage_access.id'], ),
    sa.ForeignKeyConstraint(['manage_role_id'], ['manage_role.id'], ),
    sa.PrimaryKeyConstraint('manage_access_id', 'manage_role_id')
    )
    op.create_table('manager_user_role',
    sa.Column('manage_user_id', sa.Integer(), nullable=False),
    sa.Column('manage_role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['manage_role_id'], ['manage_role.id'], ),
    sa.ForeignKeyConstraint(['manage_user_id'], ['manage_user.id'], ),
    sa.PrimaryKeyConstraint('manage_user_id', 'manage_role_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('manager_user_role')
    op.drop_table('manager_role_access')
    op.drop_index(op.f('ix_manage_user_username'), table_name='manage_user')
    op.drop_index(op.f('ix_manage_user_update_time'), table_name='manage_user')
    op.drop_index(op.f('ix_manage_user_create_time'), table_name='manage_user')
    op.drop_table('manage_user')
    op.drop_index(op.f('ix_manage_role_update_time'), table_name='manage_role')
    op.drop_index(op.f('ix_manage_role_role_name'), table_name='manage_role')
    op.drop_index(op.f('ix_manage_role_create_time'), table_name='manage_role')
    op.drop_table('manage_role')
    op.drop_index(op.f('ix_manage_access_update_time'), table_name='manage_access')
    op.drop_index(op.f('ix_manage_access_path'), table_name='manage_access')
    op.drop_index(op.f('ix_manage_access_parent_id'), table_name='manage_access')
    op.drop_index(op.f('ix_manage_access_level'), table_name='manage_access')
    op.drop_index(op.f('ix_manage_access_create_time'), table_name='manage_access')
    op.drop_table('manage_access')
    # ### end Alembic commands ###