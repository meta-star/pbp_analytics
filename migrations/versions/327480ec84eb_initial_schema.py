"""Initial schema

Revision ID: 327480ec84eb
Revises:
Create Date: 2026-01-25 06:51:24.699198

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '327480ec84eb'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create blacklist table
    op.create_table(
        'blacklist',
        sa.Column('uuid', sa.VARCHAR(36), nullable=False),
        sa.Column('url', sa.Text(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('url_hash', sa.VARCHAR(64), nullable=False),
        sa.PrimaryKeyConstraint('uuid'),
        sa.UniqueConstraint('url_hash')
    )

    # Create result_cache table
    op.create_table(
        'result_cache',
        sa.Column('url_hash', sa.VARCHAR(64), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('url_hash')
    )

    # Create trustlist table
    op.create_table(
        'trustlist',
        sa.Column('uuid', sa.VARCHAR(36), nullable=False),
        sa.Column('url', sa.Text(), nullable=False),
        # Supporting large binary for legacy narray compatibility if strictly needed,
        # but models.py defined it.
        sa.Column('target_view_narray', sa.LargeBinary().with_variant(sa.LargeBinary(length=16777215), 'mysql'), nullable=True),
        sa.Column('target_view_signature', sa.Text(), nullable=True),
        sa.Column('target_view_embedding', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('uuid')
    )

    # Create trust_domain table
    op.create_table(
        'trust_domain',
        sa.Column('uuid', sa.VARCHAR(36), nullable=False),
        sa.Column('foreign_key', sa.VARCHAR(36), nullable=False),
        sa.Column('domain', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('uuid'),
        sa.ForeignKeyConstraint(['foreign_key'], ['trustlist.uuid'], )
    )

    # Create warnlist table
    op.create_table(
        'warnlist',
        sa.Column('uuid', sa.VARCHAR(36), nullable=False),
        sa.Column('url', sa.Text(), nullable=False),
        sa.Column('origin', sa.Text(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('uuid')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('warnlist')
    op.drop_table('trust_domain')
    op.drop_table('trustlist')
    op.drop_table('result_cache')
    op.drop_table('blacklist')
