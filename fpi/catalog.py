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

    @property
    def __init_string(self):
        return 'sqlite:///%s' % self.catalog_file

    def __open_database(self):
        if database_exists(self.__init_string):
            self.__start_engine()

    def __start_engine(self):
        self.engine = create_engine(self.__init_string)
        self._session = sessionmaker(bind=self.engine)()

    def __set_catalog_name_and_file(self, catalog_name):
        def name_with_dir(a_name):
            a_basename = os.path.basename(a_name)
            return '%s/%s.fpicat' % (a_name, a_basename)

        name, ext = os.path.splitext(catalog_name)
        base = os.path.basename(name)
        catalog = catalog_name
        if os.path.exists(catalog):
            pass
        elif ext == '.fpicat':
            if name == base:
                catalog = '%s/%s%s' % (base, base, ext)
        elif os.path.isfile(catalog_name):
            msg = "Refusing to overwrite existing file: '%'" % (catalog_name)
            raise Exception(msg)
        else:
            catalog = '%s.fpicat' % catalog_name
            if not os.path.isfile(catalog):
                catalog = name_with_dir(catalog_name)
        return (base, catalog)

    def __init__(self, catalog_name):
        """Initialize a new catalog."""
        self._session = None
        cname, fname = self.__set_catalog_name_and_file(catalog_name)
        self.catalog_name = cname
        self.catalog_file = fname
        self.__open_database()

    def _check_catalog(self):
        if self._session is None:
            err = "Trying to use an inexistent catalog '%s'."
            raise Exception(err % self.catalog_name)

    @property
    def session(self):
        """Retrieve the database session."""
        self._check_catalog()
        return self._session

    def create(self):
        """Create a new catalog."""
        directory, filename = os.path.split(self.catalog_file)
        if len(directory) > 0:
            if not os.path.exists(directory):
                os.makedirs(directory)
            elif not os.path.isdir(directory):
                raise Exception("Cannot create catalog directory.")
        if database_exists(self.__init_string):
            msg = "Refusing to overwrite catalog '%s'." % self.catalog_file
            raise Exception(msg)
        else:
            self.__start_engine()
            Base.metadata.create_all(self.engine)

    _INGEST_METHOD = {
        'add': _add,
        'copy': shutil.copy2,
        'move': shutil.move
    }

    def ingest(self, method, filelist, *args, **kwargs):
        """Ingest the files in filelist using the provided method."""
        if len(filelist) == 0:
            raise Exception("No item to ingest.")
        self._check_catalog()
        if kwargs.get('session_name', None) is None:
            now = datetime.datetime.utcnow()
            kwargs['session_name'] = now.strftime("%Y-%m-%dT%H%M%S.%f%z")
        fn = Catalog._INGEST_METHOD.get(method, None)
        if fn is None:
            raise Exception("Invalid ingestion method.")

        kwargs['method'] = fn
        kwargs['sequence'] = 1

        self.__ingest_itens(filelist, kwargs)

    def __ingest_itens(self, items, options):
        for i in items:
            options['source'] = i
            if os.path.isfile(i):
                self.__ingest_file(options)
            else:
                self.__ingest_dir(options)

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
            except Exception as e:
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
            asset = dao.Asset(fname, options['session_name'])
            session.add(asset)
            image = dao.Image(asset, metadata)
            session.add(image)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            if 'NOT NULL constraint failed' in str(e):
                raise Exception("INTERNAL ERROR: Null field.")
            if 'UNIQUE constraint failed' in str(e):
                raise Exception("Ingesting an asset already in the catalog.")
            # Raise any unknown error.
            raise e
        except FileNotFoundError as fnf:
            session.rollback()
            fmt = "ORIGINAL = %s \n\n SRC = %s \n\t FNAME = %s"
            msg = fmt % (fnf, src, fname)
            raise Exception(msg)
        options['sequence'] += 1

    def __ingest_dir(self, options):
        directory = options['source']
        for entry in os.scandir(directory):
            options['source'] = entry.path
            if entry.is_file():
                self.__ingest_file(options)
            else:
                if options.get('recurse', False):
                    self.__ingest_dir(options)

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
        if object == "session":
            return self.__info_session(parameter)
        if object == "asset":
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

    def set_attributes(self, assets, options):
        """Set attributes provided in options to each of the given assets."""
        session = self.session
        for asset in assets:
            q = session.query(dao.Image).filter(dao.Image.asset_id == asset)
            for image in q:
                image.set_flag(options.get('flag', image.flag))
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            # TODO: Handle errors.
            raise e
