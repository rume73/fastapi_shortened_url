"""01_initial-db

Revision ID: cf898d235c71
Revises: 
Create Date: 2023-03-16 17:27:09.708520

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlalchemy_utils
# revision identifiers, used by Alembic.
revision = 'cf898d235c71'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('short_url',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('original_url', sqlalchemy_utils.types.url.URLType(), nullable=False),
    sa.Column('url_id', sa.String(length=8), nullable=False),
    sa.Column('short_url', sqlalchemy_utils.types.url.URLType(), nullable=False),
    sa.Column('usages_count', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_short_url_url_id'), 'short_url', ['url_id'], unique=False)
    op.create_table('short_url_history',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('short_url', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('client', sa.String(length=50), nullable=False),
    sa.Column('use_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['short_url'], ['short_url.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_short_url_history_use_at'), 'short_url_history', ['use_at'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_short_url_history_use_at'), table_name='short_url_history')
    op.drop_table('short_url_history')
    op.drop_index(op.f('ix_short_url_url_id'), table_name='short_url')
    op.drop_table('short_url')
    # ### end Alembic commands ###
