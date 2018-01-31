"""Environment preparation for testing catalog features."""

import os
import os.path


def remove_catalog(context):
    """Remove the cataog used for testing."""
    # TODO: Obtain catalog name from context.
    catalog_file = "%s.fpicat" % ("test_catalog")
    if os.path.isfile(catalog_file):
        os.unlink(catalog_file)


def before_scenario(context, scenario):
    """Execute before each scenario."""
    remove_catalog(context)


def after_feature(context, feature):
    """Execute after all tests have been executed."""
    remove_catalog(context)
