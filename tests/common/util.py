"""Common database test utilities."""

import os.path
from sqlalchemy import create_engine
from alembic.migration import MigrationContext


# Utility functions

def get_catalog_file(context):
    """Generate a catalog file name for a context."""
    assert hasattr(context, 'catalog_name')
    directory = ""
    if not context.catalog_name.startswith('./'):
        basename = os.path.basename(context.catalog_name)
        filename, ext = os.path.splitext(os.path.split(basename)[-1])
        if ext is '':
            ext = '.fpicat'
        basedir = os.path.dirname(context.catalog_name)
        directory = os.path.join(basedir, filename)
    return "%s/%s%s" % (directory, filename, ext)


def get_sqlite_init_string(context):
    """Generate the SQLite string for the catatlog for the given context."""
    return "sqlite:///%s" % get_catalog_file(context)


def check_catalog_exists(context):
    """Assert that the context catalog file exists."""
    import sqlalchemy_utils as utils
    return utils.database_exists(get_sqlite_init_string(context))


def get_catalog_revision(context):
    """Retrieve the catalog revision."""
    assert check_catalog_exists(context) is True
    engine = create_engine(get_sqlite_init_string(context))
    context = MigrationContext.configure(engine)
    return context.get_current_revision()
