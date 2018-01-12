"""Test ingestion without moving or copying files."""

from behave import given, when, then


@given('the path to an image file in its final location')
def step_configure_path_to_image_file(context):
    """Prepare context for ingesting an image."""
    e = 'the path to an image file in its final location'
    raise NotImplementedError(e)


@given('the path to a f/π catalog')
def step_configure_path_to_catalog(context):
    """Prepare context with catalog for ingestion."""
    raise NotImplementedError('STEP: Given the path to a f/π catalog')


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
