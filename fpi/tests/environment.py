"""Environment preparation for testing catalog features."""

import os
import os.path
import shutil


def remove_catalog(context):
    """Remove the cataog used for testing."""
    # TODO: Obtain catalog name from context.
    try:
        remove_tree('test_catalog')
    except Exception as e:
        try:
            os.unlink('test_catalog.fpicat')
        except Exception as e:
            pass


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
    tags = set(scenario.feature.tags + scenario.tags)
    if 'copy' in tags or 'move' in tags:
        for d in ['data/catalog', 'data/originals']:
            if os.path.isdir(d):
                remove_tree(d)
        shutil.copytree('data/samples/DCIM/100FPIAM', 'data/originals')


def before_feature(context, feature):
    """Execute befora a feature is executed."""
    if "copy" in feature.tags:
        if os.path.isdir('data/catalog'):
            remove_tree('data/catalog')


def after_feature(context, feature):
    """Execute after a feature has been executed."""
    remove_catalog(context)
    if 'copy' in feature.tags or 'move' in feature.tags:
        for d in ['data/catalog', 'data/originals']:
            if os.path.isdir(d):
                remove_tree(d)
