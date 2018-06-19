"""Steps to test system upgrade."""

from behave import given, when, then
import common.util as util
import logging
from version import Version


@given('the catalog revision is "{revision}"')
def given_catalog_revision(context, revision):
    """Ensure the catalog has the expected revision."""
    logging.getLogger("alembic").setLevel(logging.CRITICAL)
    assert revision == util.get_catalog_revision(context)


@when('I try to updated it the current version')
def when_update_to_current_version(context):
    """Update catalog to current version."""
    try:
        context.catalog.upgrade()
        context.exception = None
    except Exception as e:
        context.exception = e


@given('the catalog is ready for use in the current version')
@then('the catalog is ready for use in the current version')
def assert_catalog_has_current_version(context):
    """Assert catalog has the current version."""
    assert Version.db_revision() == util.get_catalog_revision(context)
