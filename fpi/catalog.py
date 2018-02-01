"""Functions used to manage catalogs."""

from sqlalchemy_utils import database_exists, create_database

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import datetime
import os

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

    def ingest(self, method, filelist, session_name=None, options=None):
        """Ingest the files in filelist using the provided method."""
        recurse = 'recurse' in options if options is not None else False
        if session_name is None:
            now = datetime.datetime.utcnow()
            session_name = now.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        session = self.Session()
        if method == 'add':
            for f in filelist:
                if os.path.isfile(f):
                    self.__ingest_file(session, session_name, f)
                else:
                    self.__ingest_dir(session, session_name, f, recurse)

        session.commit()

    def __ingest_dir(self, session, session_name, dirname, recurse):
        for entry in os.scandir(dirname):
            if entry.is_file():
                self.__ingest_file(session, session_name, entry.path)
            else:
                if recurse:
                    self.__ingest_dir(session, session_name, entry.path, True)

    def __ingest_file(self, session, session_name, filename):
        asset = dao.Asset(filename, session_name)
        session.add(asset)
