"""Initial migration

Revision ID: 05431401cede
Revises:
Create Date: 2023-03-31 02:22:29.766054+00:00
"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '05431401cede'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'link',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('link_url', 'link', ['url'], unique=False, postgresql_using='hash')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('link_url', table_name='link', postgresql_using='hash')
    op.drop_table('link')
    # ### end Alembic commands ###
