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


def _add(src, dest):
    pass


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

    def ingest(self, method, filelist, *args, **kwargs):
        """Ingest the files in filelist using the provided method."""
        session = self.Session()
        if kwargs.get('session_name', None) is None:
            now = datetime.datetime.utcnow()
            kwargs['session_name'] = now.strftime("%Y-%m-%dT%H%M%S.%f%z")
        if method == 'add':
            tgt = None
            fn = _add
        elif method == 'copy' or method == 'move':
            tgt = kwargs['target_dir']
            if not os.path.exists(tgt):
                os.makedirs(tgt)
            fn = shutil.copy2 if method == 'copy' else \
                shutil.move
        else:
            raise Exception("Invalid ingestion method.")

        kwargs['method'] = fn

        for f in filelist:
            kwargs['source'] = f
            if os.path.isfile(f):
                self.__ingest_file(session, kwargs)
            else:
                self.__ingest_dir(session, f, kwargs)
        session.commit()

    def __find_first(self, chlist, string):
        if string is None:
            return None
        lst = [c for c in chlist]
        return next((i for i, ch in enumerate(string) if ch in lst), None)

    def __rename(self, src, options):
        """Create a file path using the renaming rules."""
        target = options.get('target_dir', None)
        rule = options.get('rename', None)
        if target is None and rule is None:
            return src
        else:
            if rule is None:
                fname = src
            else:
                assert self.__find_first('/:\\*?', rule) is None
                rule += "{extension}"
                _, extension = os.path.splitext(options['source'])
                metadata = options.get('metadata', None)
                assert metadata is not None
                dt = metadata.capture_datetime
                rep = {"year": dt.strftime("%Y"),
                       "yy": dt.strftime("%Y"),
                       "month": dt.strftime("%m"),
                       "monthabrv": dt.strftime("%b"),
                       "day": dt.strftime("%d"),
                       "session": options['session_name'],
                       "extension": extension,
                       "ext": extension.lower()}
                fname = rule.format(**rep)
            return os.path.join(target, os.path.basename(fname))

    def __ingest_file(self, session, options):
        src = options.get('source', None)
        assert src is not None
        options['metadata'] = metadata = dao.Metadata(src)
        method = options.get('method', _add)
        fname = self.__rename(src, options)
        method(src, fname)
        asset = dao.Asset(fname, options['session_name'], metadata)
        session.add(asset)
        image = dao.Image(asset, metadata)
        session.add(image)

    def __ingest_dir(self, session, directory, options):
        recurse = options.get('recurse', False)
        for entry in os.scandir(directory):
            if entry.is_file():
                options['source'] = entry.path
                self.__ingest_file(session, options)
            else:
                if recurse:
                    self.__ingest_dir(session, entry.path, options)

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
