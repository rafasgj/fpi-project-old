"""Common database test utilities."""


def get_catalog_file(context):
    """Generate a catalog file name for a context."""
    return "%s.fpicat" % (context.catalog_name)


def get_sqlite_init_string(context):
    """Generate the SQLite string for the catatlog for the given context."""
    return "sqlite:///%s" % get_catalog_file(context)


def check_catalog_exists(context):
    """Assert that the context catalog file exists."""
    import sqlalchemy_utils as utils
    return utils.database_exists(get_sqlite_init_string(context))
