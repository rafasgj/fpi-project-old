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
        imageiptc: metadata for image information.
        keywords: store assets keywords.
        synonyms: store keywords synonyms.
        imagekeywords: map images to keywords (M:N relationship)
    """
    op.create_table(
        'imageiptc',
        sa.Column('image_id', sa.Integer,
                  sa.ForeignKey('images.id', ondelete='CASCADE'),
                  primary_key=True),
        sa.Column('caption', sa.Text, nullable=True),
        sa.Column('title', sa.String, nullable=True),
        sa.Column('creator', sa.String, nullable=True),
        sa.Column('creatoraddress', sa.String, nullable=True),
        sa.Column('creatorcity', sa.String, nullable=True),
        sa.Column('creatorregion', sa.String, nullable=True),
        sa.Column('creatorpostalcode', sa.String, nullable=True),
        sa.Column('creatorcountry', sa.String, nullable=True),
        sa.Column('creatortelephone', sa.String, nullable=True),
        sa.Column('creatoremail', sa.String, nullable=True),
        sa.Column('jobtitle', sa.String, nullable=True),
        sa.Column('city', sa.String, nullable=True),
        sa.Column('country', sa.String, nullable=True),
        sa.Column('copyright', sa.String, nullable=True),
        sa.Column('creditline', sa.String, nullable=True),
        sa.Column('headline', sa.String, nullable=True),
        sa.Column('instructions', sa.String, nullable=True),
        sa.Column('usage', sa.String, nullable=True),
        sa.Column('event', sa.String, nullable=True),
        sa.Column('copyrighturl', sa.String, nullable=True),
        sa.Column('sublocation', sa.String, nullable=True),
    )
    op.create_table(
        'keywords',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('parent_id', sa.Integer,
                  sa.ForeignKey('keywords.id', ondelete='RESTRICT')),
        sa.Column('text', sa.String, nullable=False),
        sa.Column('person', sa.Boolean, default=False),
        sa.Column('private', sa.Boolean, default=False),
        sa.Column('export_synonyms', sa.Boolean, default=False),
        sa.Column('lang', sa.String),
    )
    op.create_table(
        'synonyms',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('keyword_id', sa.Integer,
                  sa.ForeignKey('keywords.id', ondelete='CASCADE')),
        sa.Column('text', sa.String, nullable=False),
    )
    op.create_table(
        'imagekeywords',
        sa.Column('image_id', sa.Integer,
                  sa.ForeignKey('images.id', ondelete='CASCADE'),
                  primary_key=True),
        sa.Column('keyword_id', sa.Integer,
                  sa.ForeignKey('keywords.id', ondelete='CASCADE'),
                  primary_key=True),
    )


def downgrade():
    """Downgrade database to previous version."""
    op.drop_table('imageiptc')
