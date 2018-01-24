"""Tests the creation of new f/π catalogs."""

from behave import given, when, then

from common.util import check_catalog_exists, get_sqlite_init_string

import catalog
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
def step_arg_catalog_name(context, name):
    """Set the new catalog name."""
    context.catalog = name


@when('creating a new catalog')
def step_execute_catalog_creation(context):
    """Execute catalog creation."""
    try:
        catalog.init(context.catalog)
        context.exception = None
    except Exception as e:
        context.exception = e


@then('an empty catalog is created with the given name')
def step_check_catalog_is_empty_after_creation(context):
    """Create a catalog that is empty, and have the given name."""
    assert context.exception is None
    assert check_catalog_exists(context) is True


@then('there is no Asset in the catalog.')
def step_check_asset_count(context):
    """Check if there are any Asset in the catalog."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    engine = create_engine(get_sqlite_init_string(context))
    session = sessionmaker(bind=engine)()
    assert session.query(Asset).count() is 0


@given('that a catalog with the same name exists')
def step_test_when_catalog_exists(context):
    """Ensure a catalog is already created before testing."""
    if not check_catalog_exists(context):
        try:
            catalog.init(context.catalog)
        except Exception:
            pass


@then('an "{exception}" is raised saing "{msg}"')
def step_impl(context, exception, msg):
    """Test if an exception is raised when the catalog exists."""
    assert context.exception is not None
    assert isinstance(context.exception, eval(exception)) is True
    assert str(context.exception) == msg
    assert check_catalog_exists(context) is True
