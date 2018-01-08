"""Tests the creation of new f/π catalogs."""

from behave import given, when, then


@given('the option to create a new catalog')
def step_opt_catalog_create(context):
    """Prepare context for creating a new catalog."""
    err = 'STEP: Given the option to create a new catalog with a catalog name'
    raise NotImplementedError(err)


@given('a valid catalog name as {name}')
def step_arg_catalog_name(context, name):
    """Set the new catalog name."""
    error = 'a valid catalog name as {name}'.format(name=name)
    raise NotImplementedError(error)


@when('creating a new catalog')
def step_execute_catalog_creation(context):
    """Execute catalog creation."""
    error = 'STEP: When using the catalog command'
    raise NotImplementedError(error)


@then('an empty catalog is created with the given name.')
def step_check_catalog_is_empty_after_creation(context):
    """Create a catalog that is empty, and have the given name."""
    error = 'STEP: Then an empty catalog is created with the given name.'
    raise NotImplementedError(error)
