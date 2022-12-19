"""Add OAuth refresh token support

Revision ID: a209f0333f5a
Revises: 4ab54becec04
Create Date: 2022-12-18 11:26:31.976348+00:00

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'a209f0333f5a'
down_revision = '4ab54becec04'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('indieauth_access_token', schema=None) as batch_op:
        batch_op.add_column(sa.Column('refresh_token', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('was_refreshed', sa.Boolean(), server_default='0', nullable=False))
        batch_op.create_index(batch_op.f('ix_indieauth_access_token_refresh_token'), ['refresh_token'], unique=True)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('indieauth_access_token', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_indieauth_access_token_refresh_token'))
        batch_op.drop_column('was_refreshed')
        batch_op.drop_column('refresh_token')

    # ### end Alembic commands ###