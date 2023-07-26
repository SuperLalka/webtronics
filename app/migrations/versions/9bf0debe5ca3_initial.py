"""Initial

Revision ID: 9bf0debe5ca3

"""
from alembic import op
import sqlalchemy as sa


revision = '9bf0debe5ca3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.BIGINT(), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=True),
        sa.Column('email', sa.String(length=100), nullable=True),
        sa.Column('password', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
        sa.UniqueConstraint('username')
    )
    op.create_table('posts',
        sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=100), nullable=True),
        sa.Column('text', sa.Text(), nullable=True),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id', 'author_id'),
        sa.UniqueConstraint('id')
    )
    op.create_table('posts_rating',
        sa.Column('value', sa.SmallInteger(), nullable=True),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('post_id', 'user_id'),
        sa.UniqueConstraint('post_id', 'user_id', name='user_posts_ratings_idx')
    )
    op.create_index('user_posts_ratings_un', 'posts_rating', ['post_id', 'user_id'], unique=False)


def downgrade() -> None:
    op.drop_index('user_posts_ratings_un', table_name='posts_rating')
    op.drop_table('posts_rating')
    op.drop_table('posts')
    op.drop_table('users')
