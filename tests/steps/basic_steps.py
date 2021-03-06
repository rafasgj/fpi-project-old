"""Basic common steps."""

from behave import given, then

# from common.util import get_sqlite_init_string

import os.path

import catalog
import errors  # noqa: F401

from common.util import get_catalog_file


def __set_context_catalog_name(context, catalog_name):
    context.catalog_name = catalog_name
    catalog_file = get_catalog_file(context)
    context.catalog_directory = os.path.dirname(catalog_file)
    context.catalog_file = catalog_file
    context.catalog = catalog.Catalog(context.catalog_name)


# Create an empty catalog
@given('an empty catalog named "{catalog_name}"')
def given_empty_catalog(context, catalog_name):
    """Ensure the catalog with the given filename does exist."""
    context.exception = None
    __set_context_catalog_name(context, catalog_name.strip())
    context.catalog.create()
    context.session = context.catalog.session


# Set the catalog name, but don't create it.
@given('a catalog file named as "{catalog_file}"')
def given_catalog_file(context, catalog_file):
    """Set the filename of the catalog."""
    context.exception = None
    __set_context_catalog_name(context, catalog_file.strip())


@given('a catalog named "{catalog_name}"')
def given_catalog_name(context, catalog_name):
    """Set the new catalog name."""
    context.exception = None
    __set_context_catalog_name(context, catalog_name.strip())


# A catalog with some assets in it.
@given('a catalog named "{catalog_name}" with some assets')
def given_catalog_with_assets(context, catalog_name):
    """Create a catalog with some assets."""
    try:
        context.exception = None
        __set_context_catalog_name(context, catalog_name.strip())
        context.catalog.create()
        context.catalog.ingest('add', [r['filename'] for r in context.table])
    except Exception as e:
        context.exception = e


# Files that might or might not exist

@given('a file {filename}')
def given_file_name(context, filename):
    """Set file list to a single file, not checking it."""
    context.files = [filename]


# Assert that a device exists at a given mount point.

@given('a device mounted at "{mount_point}"')
def given_mount_point(context, mount_point):
    """Ensure the directory given is a mount point."""
    assert os.path.ismount(os.path.realpath(mount_point.strip())) is True


# Test exceptions

@then('an exception "{exception}" is raised')
def then_expception_raised(context, exception):
    """Test if an exception is raised."""
    assert context.exception is not None
    if not isinstance(context.exception, eval(exception)):
         raise context.exception
    assert isinstance(context.exception, eval(exception)) is True


@then('an exception "{exception}" is raised saying "{msg}"')
def then_expception_raised_with_message(context, exception, msg):
    """Test if an exception is raised."""
    assert context.exception is not None
    assert isinstance(context.exception, eval(exception)) is True
    if not str(context.exception).startswith(msg):
        raise context.exception


@then('no exception is raised')
def then_no_expception_raised(context):
    """Test if an exception is raised."""
    if context.exception is not None:
        raise context.exception


@then('the directory "{directory}" does not exist')
def then_directory_does_not_exist(context, directory):
    """Test if the given directory does not exist."""
    assert os.path.exists(directory) is False
