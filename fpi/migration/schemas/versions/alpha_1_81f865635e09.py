"""Migrate database to system version alpha_1.

Revision ID: 81f865635e09
Revises:
Create Date: 2018-05-10 11:57:12.416440
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81f865635e09'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """
    Create the initial database tables.
    The database tables for the first version include:
        assets = {
            id:string, # the md5 hash value of the asset thumbnail
            device_id:integer, # the device id of the storage device.
            path:string, # the path to the asset in the device.
            filename:string, # the asset filename
            import_time:datetime # the time when the asset was ingested.
            import_session:string # the session name.
        }
        images = {
            id: integer,
            capture_datetime:datetime, # the image capture datetime
            width:integer, # the image width
            height:integer, # the image height
        }
        Relationships:
            asset:virtual_copies 1:N image:asset_id, cascade delete.
    """
    op.create_table(
        'assets',
        sa.Column('id', sa.String, primary_key=True),
        sa.Column('device_id', sa.Integer, nullable=False),
        sa.Column('path', sa.String, nullable=False),
        sa.Column('filename', sa.String, nullable=False),
        sa.Column('import_time', sa.DateTime, nullable=False),
        sa.Column('import_session', sa.String, nullable=False)
    )
    op.create_table(
        'images',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('asset_id', sa.Integer,
                  sa.ForeignKey('assets.id', ondelete='CASCADE')),
        sa.Column('capture_datetime', sa.DateTime, nullable=False),
        sa.Column('width', sa.Integer, nullable=False),
        sa.Column('height', sa.Integer, nullable=False)
    )


def downgrade():
    """Delete created tables."""
    op.drop_table('assets')
    op.drop_table('images')
