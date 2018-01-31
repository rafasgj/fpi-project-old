"""Test ingestion without moving or copying files."""

from behave import given, when, then

from common.util import get_sqlite_init_string

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os.path

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


@given('a device mounted at "{mountpoint}"')
def given_mount_point(context, mountpoint):
    """Ensure provided mount point is correct."""
    assert os.path.ismount(mountpoint) is True
    context.mountpoint = mountpoint


@given('an image file at "{imagefile}"')
def given_path_to_image_file(context, imagefile):
    """Prepare context for ingesting an image."""
    context.files = [imagefile]


@when('ingesting assets into the catalog')
def when_ingest_by_add(context):
    """Ingest a file into the catalog and keep it where it is."""
    context.catalog.ingest(context.option, context.files)


@then('one asset is in the catalog with its attributes')
def then_one_asset_is_in_the_catalog(context):
    """Check if the asset was correctly stored in the catalog."""
    assert context.session.query(Asset).count() is 1


@then('the destination file attributes are stored within the asset')
def then_asset_destination_file_attributes_are_stored(context):
    """Check if the destination file attributes were correctly saved."""
    for device_id, filename, path in context.table:
        filename = filename.strip()
        query = context.session.query(Asset)
        asset = query.filter(Asset.filename == filename).one()
        assert asset.device_id == int(device_id.strip())
        # assert asset.device_label == device_id
        assert asset.filename == filename
        assert asset.path == path.strip()


@then('the asset id is the MD5 hash "{hashvalue}"')
def then_asset_id_is_md5_hash(context, hashvalue):
    """Check if th asset id was correctly obtained."""
    asset = context.session.query(Asset).one()
    assert asset.id == hashvalue.strip()


@given('a list of files')
def given_list_of_files(context):
    """Set list of files to be ingested."""
    context.files = [row['filename'] for row in context.table]


@then('there are {some} assets is the catalog, with its attributes')
def then_some_assets_are_stored(context, some):
    """Check if the right number of assets were added to the catalog."""
    assert context.session.query(Asset).count() is int(some)


@then('the assets id is a MD5 hash')
def then_check_assets_id_hash(context):
    """Check if th assets id was correctly obtained."""
    for filename, md5 in context.table:
        query = context.session.query(Asset)
        asset = query.filter(Asset.filename == filename.strip()).one()
        assert asset.id == md5.strip()
