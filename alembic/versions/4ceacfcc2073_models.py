"""models

Revision ID: 4ceacfcc2073
Revises: 
Create Date: 2017-08-20 12:19:57.633608

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ceacfcc2073'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('name', sa.Text, nullable=False),
    )

    op.create_table(
        'books',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('title', sa.Text, nullable=False),
        sa.Column('author', sa.Text, nullable=False),
    )

    op.create_table(
        'loans',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('user_id', sa.BigInteger, sa.ForeignKey('users.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False),
        sa.Column('book_id', sa.BigInteger, sa.ForeignKey('books.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False, unique=True),
    )
    op.create_index('loans_user_id_fkey_idx', 'loans', ['user_id'])


def downgrade():
    op.drop_table('loans')
    op.drop_table('books')
    op.drop_table('users')
