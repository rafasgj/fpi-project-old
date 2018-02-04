"""Environment preparation for testing catalog features."""

import os
import os.path


def remove_catalog(context):
    """Remove the cataog used for testing."""
    # TODO: Obtain catalog name from context.
    catalog_file = "%s.fpicat" % ("test_catalog")
    if os.path.isfile(catalog_file):
        os.unlink(catalog_file)


def remove_tree(fselement):
    """Remove the whole directory tree."""
    if os.path.isdir(fselement):
        for entry in os.scandir(fselement):
            remove_tree(entry.path)
        os.rmdir(fselement)
    else:
        os.unlink(fselement)


def before_scenario(context, scenario):
    """Execute before each scenario."""
    remove_catalog(context)


def before_feature(context, feature):
    """Execute befora a feature is executed."""
    if "copy" in feature.tags:
        remove_tree('data/catalog')


def after_feature(context, feature):
    """Execute after a feature has been executed."""
    remove_catalog(context)
