"""Functions used to manage catalogs."""

from sqlalchemy_utils import database_exists

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

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
        if database_exists(init_string):
            self.engine = create_engine(init_string)
            self.Session = sessionmaker(bind=self.engine)

    def _check_catalog(self):
        if self.__dict__.get("engine", None) is None:
            err = "Trying to use an inexistent catalog '%s'."
            raise Exception(err % self.catalog_name)

    @property
    def session(self):
        """Retrieve the database session."""
        self._check_catalog()
        return self.Session()

    def create(self):
        """Create a new catalog."""
        init_string = self.__get_catalog_init_string()
        if not database_exists(init_string):
            self.engine = create_engine(init_string)
            self.Session = sessionmaker(bind=self.engine)
            Base.metadata.create_all(self.engine)
        else:
            raise Exception("Refusing to overwrite catalog.")

    def ingest(self, method, filelist, *args, **kwargs):
        """Ingest the files in filelist using the provided method."""
        self._check_catalog()
        if kwargs.get('session_name', None) is None:
            now = datetime.datetime.utcnow()
            kwargs['session_name'] = now.strftime("%Y-%m-%dT%H%M%S.%f%z")
        if method == 'add':
            fn = _add
        elif method == 'copy':
            fn = shutil.copy2
        elif method == 'move':
            fn = shutil.move
        else:
            raise Exception("Invalid ingestion method.")

        kwargs['method'] = fn
        kwargs['sequence'] = 1

        for f in filelist:
            kwargs['source'] = f
            if os.path.isfile(f):
                self.__ingest_file(kwargs)
            else:
                self.__ingest_dir(f, kwargs)

    def __find_first(self, chlist, string):
        if string is None:
            return None
        lst = [c for c in chlist]
        return next((i for i, ch in enumerate(string) if ch in lst), None)

    def _format_fs_rule(self, rule, options):
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
               "ext": extension.lower(),
               "seq": options.get("sequence", 1)
               }
        return rule.format(**rep)

    def __rename(self, src, target, options):
        """Create a file path using the renaming rules."""
        rule = options.get('rename', None)
        if target is None and rule is None:
            return src
        else:
            if rule is None:
                fname = src
            else:
                rule += "{extension}"
                fname = self._format_fs_rule(rule, options)
                assert self.__find_first('/:\\*?}{', fname) is None
            return os.path.join(target, os.path.basename(fname))

    def _make_dirs(self, src, options):
        gen = options.get('directory_rule', None)
        tgt = options['target_dir']
        if gen is not None:
            tgt = os.path.join(tgt, self._format_fs_rule(gen, options))
        if not os.path.exists(tgt):
            try:
                os.makedirs(tgt)
            except:
                raise Exception("Cannot use target directory.")
        else:
            if not os.path.isdir(tgt):
                raise Exception("Cannot use target directory.")
        return tgt

    def __ingest_file(self, options):
        fname = src = options.get('source', None)
        assert src is not None
        options['metadata'] = metadata = dao.Metadata(src)
        method = options.get('method', _add)
        if method != _add:
            target = self._make_dirs(src, options)
            fname = self.__rename(src, target, options)
        method(src, fname)
        session = self.session
        try:
            asset = dao.Asset(fname, options['session_name'], metadata)
            session.add(asset)
            image = dao.Image(asset, metadata)
            session.add(image)
            session.commit()
        except IntegrityError as e:
            raise Exception("Ingesting an asset already in the catalog.")
        options['sequence'] += 1

    def __ingest_dir(self, directory, options):
        recurse = options.get('recurse', False)
        for entry in os.scandir(directory):
            if entry.is_file():
                options['source'] = entry.path
                self.__ingest_file(options)
            else:
                if recurse:
                    self.__ingest_dir(entry.path, options)

    def search(self):
        """Search for assets in the catalog."""
        return self.session.query(dao.Asset).all()

    def sessions(self):
        """Search for assets in the catalog."""
        field = dao.Asset.import_session
        query = self.session.query(field).group_by(field)
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
        query = self.session.query(dao.Asset).order_by(dao.Asset.import_time)
        items = query.filter(dao.Asset.import_session == session_id).all()
        time = items[0].import_time
        assets = [RS(id=a.id, fullpath=a.fullpath) for a in items]
        return SI(session_name=session_id, creation_time=time,
                  assets=assets)

    def __info_asset(self, asset_id):
        result = self.session.query(dao.Asset).filter(dao.Asset.id == asset_id)
        return result.one()
