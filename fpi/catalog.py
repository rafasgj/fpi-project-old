"""Functions used to manage catalogs."""

from sqlalchemy_utils import database_exists, create_database

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()


class Catalog(object):
    """Implements the abstraction of a DAM Catalog."""

    def __get_catalog_filename(self, catalog):
        """Given a catalog name or filename, return the catalog filename."""
        if catalog.endswith('.fipcat'):
            return catalog
        return "%s.fpicat" % (catalog)

    def __get_catalog_init_string(self, catalog):
        """Given a catalog name or filename, return its init string."""
        return "sqlite:///%s" % (self.__get_catalog_filename(catalog))

    def __init__(self, catalog_name):
        """Initialize a new catalog."""
        init_string = self.__get_catalog_init_string(catalog_name)
        self.engine = create_engine(init_string)
        self.Session = sessionmaker(bind=self.engine)
        if not database_exists(init_string):
            create_database(init_string)
            Base.metadata.create_all(self.engine)
        else:
            raise Exception("Refusing to overwrite catalog.")
