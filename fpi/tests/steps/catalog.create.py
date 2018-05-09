"""Tests for the creation of new f/π catalogs."""

from behave import given, when, then

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import os.path

from common.util import check_catalog_exists, \
    get_sqlite_init_string, \
    get_catalog_file

from catalog import Catalog
from dao import Asset
import errors


def __set_context_catalog_name(context, catalog_name):
    context.catalog_name = catalog_name
    catalog_file = get_catalog_file(context)
    context.catalog_directory = os.path.dirname(catalog_file)
    context.catalog_file = catalog_file


@given('an existing catalog named "{catalog_name}"')
def given_existing_catalog(context, catalog_name):
    """Set the catalog name, or raise an error if it does not exist."""
    # TODO: Make this configurable.
    os.chdir("data/versions")
    # TODO: Could be used to check DB version.
    context.command = "info"
    __set_context_catalog_name(context, catalog_name)
    if not check_catalog_exists(context):
        raise Exception("Given catalog should exist.")


@when('I try to open the catalog')
def when_open_catalog(context):
    """Open an existing catalog."""
    if not check_catalog_exists(context):
        raise Exception("Given catalog should exist.")
    try:
        context.catalog = Catalog(context.catalog_name)
        context.exception = None
    except Exception as e:
        context.exception = e


@then('it warns that the catalog is of an unexpected version')
def then_catalog_has_unexpected_version(context):
    """Check if opening a catalog raised UnexpectedCatalogVersion exception."""
    assert isinstance(context.exception, errors.UnexpectedCatalogVersion)


@given('the command to manage a catalog')
def step_command_catalog_mgmt(context):
    """Set command to catalog management."""
    context.command = "catalog"


@given('the option to create a new catalog')
def step_opt_catalog_create(context):
    """Set option to create a catalog."""
    context.option = 'new'


@given('a catalog named "{catalog_name}"')
def given_catalog_name(context, catalog_name):
    """Set the new catalog name."""
    __set_context_catalog_name(context, catalog_name)


@given('that a catalog with the same name exists')
def given_a_catalog_already_exists(context):
    """Ensure a catalog is already created before testing."""
    if not check_catalog_exists(context):
        try:
            Catalog(context.catalog_name).create()
        except Exception:
            pass


@when('creating a new catalog')
def when_creating_new_catalog(context):
    """Execute catalog creation."""
    try:
        context.catalog = Catalog(context.catalog_name)
        context.catalog.create()
        context.exception = None
    except Exception as e:
        context.exception = e


@then('an empty catalog is created with the given name')
def then_check_catalog_is_empty_after_creation(context):
    """Create a catalog that is empty, and have the given name."""
    assert context.exception is None
    if check_catalog_exists(context) is False:
        raise Exception("FAILED: %s" % context.catalog_name)
    assert check_catalog_exists(context) is True
    engine = create_engine(get_sqlite_init_string(context))
    session = sessionmaker(bind=engine)()
    assert session.query(Asset).count() is 0


@then('a directory with the catalog name exists with the catalog file inside')
def then_check_directory_with_catalog(context):
    """Check if the catalog was created inside a directory."""
    import time
    time.sleep(5)
    assert os.path.isdir(context.catalog_directory) is True
    assert os.path.isfile(context.catalog_file) is True
