"""Test ingestion without moving or copying files."""

from behave import given, when, then

from common.util import get_sqlite_init_string

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dao import Asset
import catalog


@given('the command to ingest assets')
def given_command_ingest(context):
    """Set command to ingest assets into a catalog."""
    context.command = 'ingest'


@given('an empty catalog file named "{filename}"')
def given_empty_catalog(context, filename):
    """Ensure the catalog with the given filename does exist."""
    context.catalog_name = filename[:-7] if filename.endswith(".fpicat") \
        else filename
    context.engine = create_engine(get_sqlite_init_string(context))
    context.session = sessionmaker(bind=context.engine)()
    context.catalog_file = filename
    context.catalog = catalog.Catalog(context.catalog_file)
    context.catalog.create()


@given('the option to add a new file at its position')
def given_option_add(context):
    """Prepare context for creating a new catalog."""
    context.option = 'add'


@given('an image file at "{imagefile}"')
def given_path_to_image_file(context, imagefile):
    """Prepare context for ingesting an image."""
    context.filepath = imagefile


@when('ingesting assets into the catalog')
def when_ingest_by_add(context):
    """Ingest a file into the catalog and keep it where it is."""
    context.catalog.ingest([context.filepath], context.option)


@then('one asset is in the catalog with its attributes')
def check_if_asset_is_in_the_catalog(context):
    """Check if the asset was correctly stored in the catalog."""
    assert context.session.query(Asset).count() is 1


@then('the original file attributes are stored within the asset')
def asset_original_file_attributes(context):
    """Verify original file attributes stored within the asset."""
    expected = context.table.row[1]
    asset = context.session.query(Asset).one()
    assert asset.original_device_id is expected['device_id']
    assert asset.original_inode is expected['inode']
    assert asset.original_filename is expected['filename']
    assert asset.original_path is expected['path']
    assert asset.original_size is expected['size']


@then('the destination file attributes are stored within the asset')
def asset_destination_file_attributes(context):
    """Check if the destination file attributes were correctly saved."""
    expected = context.table.row[1]
    asset = context.session.query(Asset).one()
    assert asset.device_id == expected['device_id']
    assert asset.device_label == expected['device_id']
    assert asset.filename == expected['filename']
    assert asset.path == expected['path']


@then('the asset id is the MD5 hash "{md5_hash}".')
def asset_id_is_correctly_computed(context, md5_hash):
    """Check if th asset id was correctly obtained."""
    asset = context.session.query(Asset).one()
    assert asset.device_id == md5_hash
