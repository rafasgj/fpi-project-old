"""Tests for the creation of new f/π catalogs."""

from behave import given, when, then

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from common.util import check_catalog_exists, get_sqlite_init_string

from catalog import Catalog
from dao import Asset


@given('the command to manage a catalog')
def step_command_catalog_mgmt(context):
    """Set command to catalog management."""
    context.command = "catalog"


@given('the option to create a new catalog')
def step_opt_catalog_create(context):
    """Set option to create a catalog."""
    context.option = 'new'


@given('a catalog named "{name}"')
def given_catalog_name(context, name):
    """Set the new catalog name."""
    context.catalog_name = name


@when('creating a new catalog')
def step_execute_catalog_creation(context):
    """Execute catalog creation."""
    try:
        Catalog(context.catalog_name).create()
        context.exception = None
    except Exception as e:
        context.exception = e


@then('an empty catalog is created with the given name')
def step_check_catalog_is_empty_after_creation(context):
    """Create a catalog that is empty, and have the given name."""
    assert context.exception is None
    assert check_catalog_exists(context) is True
    engine = create_engine(get_sqlite_init_string(context))
    session = sessionmaker(bind=engine)()
    assert session.query(Asset).count() is 0


@given('that a catalog with the same name exists')
def given_a_catalog_already_exists(context):
    """Ensure a catalog is already created before testing."""
    if not check_catalog_exists(context):
        try:
            Catalog(context.catalog_name).create()
        except Exception:
            pass
