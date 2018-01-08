"""Functions used to manage catalogs."""

from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists


def init(catalog_name):
    """Initialize a new catalog."""
    catalog_file = "%s.fpicat" % (catalog_name)
    dbfile = "sqlite:///%s" % (catalog_file)
    engine = create_engine(dbfile)
    if not database_exists(dbfile):
        create_database(engine.url)
    else:
        raise Exception("Refusing to overwrite catalog.")
