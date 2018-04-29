"""Common database test utilities."""

import os.path


# Utility functions

def get_catalog_file(context):
    """Generate a catalog file name for a context."""
    directory = ""
    if not context.catalog_name.startswith('./'):
        basename = os.path.basename(context.catalog_name)
        filename, ext = os.path.splitext(os.path.split(basename)[-1])
        if ext is '':
            ext = '.fpicat'
        basedir = "/".join(os.path.split(basename)[:-1])
        directory = os.path.join(basedir, filename)
    return "%s/%s%s" % (directory, filename, ext)


def get_sqlite_init_string(context):
    """Generate the SQLite string for the catatlog for the given context."""
    return "sqlite:///%s" % get_catalog_file(context)


def check_catalog_exists(context):
    """Assert that the context catalog file exists."""
    import sqlalchemy_utils as utils
    return utils.database_exists(get_sqlite_init_string(context))
