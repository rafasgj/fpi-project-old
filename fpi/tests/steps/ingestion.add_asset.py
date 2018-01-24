"""Test ingestion without moving or copying files."""

from behave import given, when, then

import catalog


@given('the command to ingest assets')
def step_command_ingest(context):
    """Set command to ingest assets into a catalog."""
    context.command = 'ingest'


@given('the option to add a new file at its position')
def step_option_add(context):
    """Prepare context for creating a new catalog."""
    context.option = 'add'


@given('an image file at its destination location of "{imagefile}"')
def step_path_to_image_file(context, imagefile):
    """Prepare context for ingesting an image."""
    context.filepath = imagefile


@given('a catalog file named "{filename}"')
def step_ensure_catalog_exists(context, filename):
    """Ensure the catalog with the given filename does exist."""
    if filename.endswith('.fpicat'):
        filename = filename[:-7]
    context.catalog_file = filename
    catalog.init(context.catalog)


@when('ingesting assets into the catalog and keep its location')
def step_ingest_by_add(context):
    """Ingest a file into the catalog and keep it where it is."""
    e = 'STEP: When ingesting assets into the system and keep its location'
    raise NotImplementedError(e)


@then('the file metadata is found in the catalog.')
def step_check_if_asset_is_in_the_catalog(context):
    """Check if the asset was correctly stored in the catalog."""
    e = 'STEP: Then the file metadata is found in the catalog.'
    raise NotImplementedError(e)
