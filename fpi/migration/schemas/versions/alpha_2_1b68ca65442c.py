"""Migrate database to system version alpha_2.

Revision ID: 1b68ca65442c
Revises: 81f865635e09
Create Date: 2018-05-10 14:22:35.439032

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b68ca65442c'
down_revision = '81f865635e09'
branch_labels = None
depends_on = None


def upgrade():
    """
    Add attributes to the images.
    The following changes are added to the catalog:
        images = {
            flag:integer, # 0 not-flagged, 1 flagged, 2 rejected
            label:string, # a label name for the image.
            label_color:integer, # an RGB triplet (24-bit, masked 0x0FFF)
            rating:integer, # the image rating, 0 to 5.
        }
    """
    image_columns = [
        sa.Column('flag', sa.Integer, nullable=True, default='0'),
        # sa.Column('label', sa.String, nullable=True),
        # sa.Column('label_color', sa.Integer, nullable=True),
        # sa.Column('rating', sa.Integer, nullable=True, default='0')
    ]
    for column in image_columns:
        op.add_column('images', column)


def downgrade():
    """Downgrade database to previous version."""
    image_columns = ['flag', 'label', 'labelColor', 'rating']
    for column in image_columns:
        op.drop_column('images', column)
