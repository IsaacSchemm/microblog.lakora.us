"""Allow activity forwarding

Revision ID: 93e36ff5c691
Revises: ba131b14c3a1
Create Date: 2022-07-06 09:03:57.656539

"""
import sqlalchemy as sa
from sqlalchemy.schema import CreateTable

from alembic import op
from app.database import engine
from app.models import OutgoingActivity

# revision identifiers, used by Alembic.
revision = '93e36ff5c691'
down_revision = 'ba131b14c3a1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_inbox_activity_object_ap_id'), 'inbox', ['activity_object_ap_id'], unique=False)
    op.create_index(op.f('ix_inbox_ap_type'), 'inbox', ['ap_type'], unique=False)
    op.create_index(op.f('ix_outbox_activity_object_ap_id'), 'outbox', ['activity_object_ap_id'], unique=False)
    op.create_index(op.f('ix_outbox_ap_type'), 'outbox', ['ap_type'], unique=False)
    # ### end Alembic commands ###
    # XXX: cannot remove alter to make a column nullable, we have to drop/recreate it
    create_statement = CreateTable(OutgoingActivity.__table__).compile(engine)
    op.execute("DROP TABLE IF EXISTS outgoing_activity;")
    op.execute(f"{create_statement};")
    # Instead of this:
    # op.add_column('outgoing_activity', sa.Column('inbox_object_id', sa.Integer(), nullable=True))
    # op.alter_column('outgoing_activity', 'outbox_object_id',
    #           existing_type=sa.INTEGER(),
    #           nullable=True)
    # op.create_foreign_key(None, 'outgoing_activity', 'inbox', ['inbox_object_id'], ['id'])
    # op.create_foreign_key(None, 'outgoing_activity', 'outbox', ['outbox_object_id'], ['id'])


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("outgoing_activity")
    op.create_table('outgoing_activity',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('recipient', sa.String(), nullable=False),
    sa.Column('outbox_object_id', sa.Integer(), nullable=False),
    sa.Column('tries', sa.Integer(), nullable=False),
    sa.Column('next_try', sa.DateTime(timezone=True), nullable=True),
    sa.Column('last_try', sa.DateTime(timezone=True), nullable=True),
    sa.Column('last_status_code', sa.Integer(), nullable=True),
    sa.Column('last_response', sa.String(), nullable=True),
    sa.Column('is_sent', sa.Boolean(), nullable=False),
    sa.Column('is_errored', sa.Boolean(), nullable=False),
    sa.Column('error', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['outbox_object_id'], ['outbox.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index(op.f('ix_outbox_ap_type'), table_name='outbox')
    op.drop_index(op.f('ix_outbox_activity_object_ap_id'), table_name='outbox')
    op.drop_index(op.f('ix_inbox_ap_type'), table_name='inbox')
    op.drop_index(op.f('ix_inbox_activity_object_ap_id'), table_name='inbox')
    # ### end Alembic commands ###
