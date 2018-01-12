"""Tests the creation of new f/π catalogs."""

from behave import given, when, then

import catalog


def check_catalog_exists(context):
    """Assert that the context catalog file exists."""
    import sqlalchemy_utils as utils
    catalog_file = "%s.fpicat" % (context.catalog)
    catalogdb = "sqlite:///%s" % (catalog_file)
    return utils.database_exists(catalogdb)


@given('the option to create a new catalog')
def step_opt_catalog_create(context):
    """Prepare context for creating a new catalog."""
    context.command = 'catalog'
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
    raise NotImplementedError('there is no asset in the catalog')


@given('the catalog exists')
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
