"""Basic common steps."""

from behave import given, then

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from common.util import get_sqlite_init_string

import os.path

import catalog


# Create an empty catalog

@given('an empty catalog file named "{filename}"')
def given_empty_catalog(context, filename):
    """Ensure the catalog with the given filename does exist."""
    context.catalog_name = filename
    context.engine = create_engine(get_sqlite_init_string(context))
    context.session = sessionmaker(bind=context.engine)()
    context.catalog = catalog.Catalog(context.catalog_name)
    context.catalog.create()


# Files that might or might not exist

@given('a file {filename}')
def given_file_name(context, filename):
    """Set file list to a single file, not checking it."""
    context.files = [filename]


# Assert that a device exists at a given mount point.

@given('a device mounted at "{mount_point}"')
def given_mount_point(context, mount_point):
    """Ensure the directory given is a mount point."""
    assert os.path.ismount(os.path.realpath(mount_point)) is True


# Test exceptions

@then('an "{exception}" is raised saing "{msg}"')
def then_expception_raised_during_operatiion(context, exception, msg):
    """Test if an exception is raised."""
    assert context.exception is not None
    assert isinstance(context.exception, eval(exception)) is True
    assert str(context.exception) == msg


@then('no exception is raised')
def then_no_expception_raised(context):
    """Test if an exception is raised."""
    if context.exception is not None:
        raise context.exception
