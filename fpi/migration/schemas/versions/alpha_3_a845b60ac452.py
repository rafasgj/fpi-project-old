"""Migrate database to system version alpha_3.

Revision ID: a845b60ac452
Revises: 1b68ca65442c
Create Date: 2018-06-23 22:56:12.808894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a845b60ac452'
down_revision = '1b68ca65442c'
branch_labels = None
depends_on = None


def upgrade():
    """
    Add support for several IPTC attributes.
    The following changes are added to the catalog:
        imageiptc = {
            id: integer, ForeignKey(images.id)
            caption:Text
        }
    """
    op.create_table(
        'imageiptc',
        sa.Column('image_id', sa.String,
                  sa.ForeignKey('images.id', ondelete='CASCADE'),
                  primary_key=True),
        sa.Column('caption', sa.Text, nullable=True),
        sa.Column('title', sa.String, nullable=True),
        sa.Column('creator', sa.String, nullable=True),
        sa.Column('jobtitle', sa.String, nullable=True),
        sa.Column('city', sa.String, nullable=True),
        sa.Column('country', sa.String, nullable=True),
        sa.Column('copyright', sa.String, nullable=True),
        sa.Column('creditline', sa.String, nullable=True),
        sa.Column('headline', sa.String, nullable=True),
    )


def downgrade():
    """Downgrade database to previous version."""
    op.drop_table('imageiptc')
