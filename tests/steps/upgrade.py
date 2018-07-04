"""Steps to test system upgrade."""

from behave import given, when, then
import common.util as util
import logging
from version import Version
from catalog import Catalog


@given('the catalog revision is "{revision}"')
def given_catalog_revision(context, revision):
    """Ensure the catalog has the expected revision."""
    logging.getLogger("alembic").setLevel(logging.CRITICAL)
    assert revision == util.get_catalog_revision(context)


@given('the catalog is ready for use in the current version')
@then('the catalog is ready for use in the current version')
def assert_catalog_has_current_version(context):
    """Assert catalog has the current version."""
    assert Version.db_revision() == util.get_catalog_revision(context)


@when('I try to update it the current version')
def when_update_to_current_version(context):
    """Update catalog to current version."""
    try:
        context.catalog.upgrade()
        context.exception = None
    except Exception as e:
        context.exception = e


@when('I request the version of a catalog that does not exist.')
def when_verify_version_of_inexistent_catalog(context):
    """Try to verify the version of an inexistent catalog."""
    context.revision = False
    try:
        context.revision = Catalog("inexistent_catalog").revision
    except Exception as e:
        context.exception = e
