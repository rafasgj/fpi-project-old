"""Functions used to manage catalogs."""

from sqlalchemy_utils import database_exists, create_database

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import datetime

from base import Base

import dao


class Catalog(object):
    """Implements the abstraction of a DAM Catalog."""

    @classmethod
    def __get_catalog_filename(self, catalog):
        """Given a catalog name or filename, return the catalog filename."""
        if catalog.endswith('.fpicat'):
            return catalog
        return "%s.fpicat" % (catalog)

    def __get_catalog_init_string(self):
        """Given a catalog name or filename, return its init string."""
        filename = Catalog.__get_catalog_filename(self.catalog_name)
        return "sqlite:///%s" % (filename)

    def __init__(self, catalog_name):
        """Initialize a new catalog."""
        self.catalog_name = catalog_name
        init_string = self.__get_catalog_init_string()
        self.engine = create_engine(init_string)
        self.Session = sessionmaker(bind=self.engine)

    def create(self):
        """Create a new catalog."""
        init_string = self.__get_catalog_init_string()
        if not database_exists(init_string):
            create_database(init_string)
            Base.metadata.create_all(self.engine)
        else:
            raise Exception("Refusing to overwrite catalog.")

    def ingest(self, method, filelist, session_name=None):
        """Ingest the files in filelist using the provided method."""
        if session_name is None:
            now = datetime.datetime.utcnow()
            session_name = now.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        session = self.Session()
        if method == 'add':
            for file in filelist:
                asset = dao.Asset(file, session_name)
                session.add(asset)
        session.commit()
