"""Test de Asset data object."""

from behave import given, when, then

from catalog import Catalog


@given('the command to list assets in the catalog')
def given_command_list(context):
    """Set command to 'list'."""
    context.command = 'list'


@given('a catalog file named as "{catalog_file}"')
def givent_c(context, catalog_file):
    """Set the filename of the catalog."""
    context.catalog_file = catalog_file


@given('the catalog has some assets')
def given_filename_list(context):
    """Add given filenames to the catalog."""
    context.files = [row['filename'] for row in context.table]
    context.catalog = Catalog(context.catalog_file)
    context.catalog.create()
    context.catalog.ingest("add", context.files)


@when('listing all assets in the catalog')
def when_listing_assets(context):
    """List all the assets in the catalog."""
    context.result = context.catalog.search()


@then('I expect all the assets to be listed, with their id and full path')
def then_compare_filenames_and_ids(context):
    """Compare filename/id obtained with expected ones."""
    for row in context.table:
        for asset in context.result:
            if asset.fullpath == row['fullpath']:
                assert asset.id is row['id']
                break
