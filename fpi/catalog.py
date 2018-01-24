"""Functions used to manage catalogs."""

import dbutil

from sqlalchemy_utils import database_exists, create_database


def init(catalog_name):
    """Initialize a new catalog."""
    dbutil.init(catalog_name)
    dbfile = dbutil.get_catalog_init_string(catalog_name)
    if not database_exists(dbfile):
        create_database(dbfile)
        dbutil.Base.metadata.create_all(dbutil.engine)
    else:
        raise Exception("Refusing to overwrite catalog.")
