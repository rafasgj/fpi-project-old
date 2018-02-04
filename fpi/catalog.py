"""Functions used to manage catalogs."""

from sqlalchemy_utils import database_exists, create_database

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import datetime
import os
import shutil
from collections import namedtuple

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

    def ingest(self, method, filelist, session_name=None, *args, **kwargs):
        """Ingest the files in filelist using the provided method."""
        recurse = kwargs.get('recurse', False)
        if session_name is None:
            now = datetime.datetime.utcnow()
            session_name = now.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        session = self.Session()
        if method == 'add':
            target_dir = None
        elif method == "copy":
            target_dir = kwargs['target_dir']
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
        else:
            raise Exception("Invalid ingestion method.")

        for f in filelist:
            if os.path.isfile(f):
                self.__ingest_file(session, session_name, f, target_dir)
            else:
                self.__ingest_dir(session, session_name,
                                  f, target_dir, recurse)
        session.commit()

    def __ingest_file(self, session, session_name, src, target_dir=None):
        if target_dir is None:
            fname = src
        else:
            fname = os.path.join(target_dir, os.path.basename(src))
            shutil.copy2(src, fname)
        asset = dao.Asset(fname, session_name)
        session.add(asset)
        image = dao.Image(asset, fname)
        session.add(image)

    def __ingest_dir(self, session, session_name, dirname, tgt, recurse):
        for entry in os.scandir(dirname):
            if entry.is_file():
                if tgt is None:
                    fname = None
                else:
                    fname = os.path.join(tgt, os.path.basename(entry.path))
                self.__ingest_file(session, session_name,
                                   entry.path, fname)
            else:
                if recurse:
                    self.__ingest_dir(session, session_name,
                                      entry.path, tgt, True)

    def search(self):
        """Search for assets in the catalog."""
        session = self.Session()
        return session.query(dao.Asset).all()

    def sessions(self):
        """Search for assets in the catalog."""
        session = self.Session()
        field = dao.Asset.import_session
        query = session.query(field).group_by(field)
        return [s.import_session for s in query.all()]

    def info(self, object, parameter):
        """Get information about an object, given its identifier."""
        if object is "session":
            return self.__info_session(parameter)
        if object is "asset":
            return self.__info_asset(parameter)
        else:
            raise Exception("Invalid object.")

    def __info_session(self, session_id):
        SI = namedtuple('SessionInfo',
                        'session_name creation_time assets')
        RS = namedtuple('SessionAsset', 'id fullpath')
        session = self.Session()
        query = session.query(dao.Asset).order_by(dao.Asset.import_time)
        items = query.filter(dao.Asset.import_session == session_id).all()
        time = items[0].import_time
        assets = [RS(id=a.id, fullpath=a.fullpath) for a in items]
        return SI(session_name=session_id, creation_time=time,
                  assets=assets)

    def __info_asset(self, asset_id):
        session = self.Session()
        result = session.query(dao.Asset).filter(dao.Asset.id == asset_id)
        return result.one()
