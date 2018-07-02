"""Functions used to manage catalogs."""

from sqlalchemy_utils import database_exists

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from sqlalchemy import event
from sqlalchemy.engine import Engine


import datetime
import os
import os.path
import shutil
from collections import namedtuple

import logging
from alembic.migration import MigrationContext

import alembic.config
import alembic.command

import dao
import errors
from version import Version


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Configure SQLite to respect case sensitivity in LIKE."""
    cursor = dbapi_connection.cursor()
    cursor.execute('pragma case_sensitive_like=ON')
    cursor.close()


class Catalog(object):
    """Implements the abstraction of a DAM Catalog."""

    # Constants required for catalog upgrade.
    __fpi_dir = os.path.dirname(os.path.realpath(__file__))
    __PATH = os.path.join(__fpi_dir, "migration")
    __migration_config = os.path.join(__PATH, "fpi.ini")
    __migration_scripts = os.path.join(__PATH, "schemas")

    def __add(src, dest):
        pass

    def __init__(self, catalog_name):
        """Initialize a new catalog."""
        self._session = None
        cname, fname = self.__set_catalog_name_and_file(catalog_name)
        self._catalog_name = cname
        self._catalog_file = fname
        self._engine = create_engine(self.__init_string)

    @property
    def __init_string(self):
        return 'sqlite:///%s' % self._catalog_file

    @property
    def revision(self):
        """Query the database revision."""
        if self._engine is None:
            return ""
        logging.getLogger("alembic").setLevel(logging.CRITICAL)
        context = MigrationContext.configure(self._engine.connect())
        rev = context.get_current_revision()
        return rev

    def open(self):
        """Open the database for use."""
        if self._session is not None:
            return
        if database_exists(self.__init_string):
            self._engine = create_engine(self.__init_string)
            if not Version.version_match(self.revision):
                msg = "Catalog needs to be upgraded."
                raise errors.UnexpectedCatalogVersion(msg)
            self._session = sessionmaker(bind=self._engine)()
        else:
            msg = "Catalog not found: %s" % (self._catalog_file)
            raise errors.InexistentCatalog(msg)

    def __set_catalog_name_and_file(self, catalog_name):
        name, ext = os.path.splitext(catalog_name)
        dirname = os.path.dirname(name)
        base = os.path.basename(name)
        catalog = catalog_name
        if not dirname:
            catalog = "%s/%s" % (base, catalog)
        if ext == '.fpicat':
            pass
        else:
            catalog = '%s/%s.fpicat' % (name, base)
        return (base, catalog)

    def _check_catalog(self):
        if self._session is None:
            err = "Catalog '%s' has not been opened."
            raise Exception(err % self._catalog_name)

    def upgrade(self):
        """Upgrade catalog to the latest version."""
        try:
            self.open()
        except errors.UnexpectedCatalogVersion as e:
            self.__perform_upgrade()
        except Exception:
            raise
        else:
            msg = "Catalog is in the current version."
            raise errors.UnexpectedCatalogVersion(msg)

    def __perform_upgrade(self):
        alembic_cfg = alembic.config.Config(Catalog.__migration_config)
        alembic_cfg.set_main_option("sqlalchemy.url", self.__init_string)
        alembic_cfg.set_main_option("script_location",
                                    Catalog.__migration_scripts)
        alembic.command.upgrade(alembic_cfg, "head")

    @property
    def session(self):
        """Retrieve the database session."""
        self._check_catalog()
        return self._session

    def create(self):
        """Create a new catalog."""
        if self._session is not None:
            raise Exception("Catalog is already created and opened.")
        directory, filename = os.path.split(self._catalog_file)
        if len(directory) > 0:
            if not os.path.exists(directory):
                os.makedirs(directory)
            elif not os.path.isdir(directory):
                raise Exception("Cannot create catalog directory.")
        if database_exists(self.__init_string):
            msg = "Refusing to overwrite catalog '%s'." % self._catalog_file
            raise Exception(msg)
        elif os.path.isfile(self._catalog_file):
            msg = "Refusing to overwrite file '%s'." % self._catalog_file
            raise Exception(msg)
        else:
            self.__perform_upgrade()
            self._engine = create_engine(self.__init_string)
            self._session = sessionmaker(bind=self._engine)()

    _INGEST_METHOD = {
        'add': __add,
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
        method = options.get('method', Catalog.__add)
        if method is not Catalog.__add:
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

    def search(self, options=None):
        """Search for assets in the catalog."""
        self._check_catalog()
        images = self.session.query(dao.Image)
        if options is not None:
            filters = {
                'flag': (self._filter_set, dao.Image),
                'label': (self._filter_str, dao.Image),
                'rating': (self._filter_num, dao.Image),
                'filename': (self._filter_str, dao.Asset),
                'import_session': (self._filter_str, dao.Asset),
                'capture_datetime': (self._filter_date, dao.Image),
            }
            for field, value_op in options.items():
                filter_fn, table = filters.get(field, (None, None))
                if filter_fn is not None:
                    if table != dao.Image:
                        images = images.join(table)
                    images = filter_fn(images, getattr(table, field), value_op)
        return images.all()

    def _filter_set(self, images, column, values):
        if values is not None:
            if not (isinstance(values, list) or isinstance(values, set)):
                values = [values]
            if len(values) > 0:
                images = images.filter(column.in_(values))
        return images

    def _filter_num(self, images, column, value_op):
        if value_op is not None:
            op, value = value_op
            if isinstance(value, list) or isinstance(value, set):
                return self._filter_set(images, column, value)
            images = images.filter(column.op(op)(value))
        return images

    def _filter_date(self, images, column, values):
        if values is not None:
            start = values.get('start', None)
            end = values.get('end', None)
            if start is not None:
                images = images.filter(column.op(">=")(start))
            if end is not None:
                images = images.filter(column.op("<=")(end))
        return images

    def _filter_str(self, images, column, value_op):
        if value_op is not None:
            op, value = value_op
            if isinstance(value, list) or isinstance(value, set):
                return self._filter_set(images, column, value_op)
            if op.get('partial', False):
                value = "%%%s%%" % value
            operator = column.ilike if op.get('caseinsensitive', True) \
                else column.like
            operator = ~operator if op.get('not', False) else operator
            images = images.filter(operator(value))
        return images

    def sessions(self):
        """Search for assets in the catalog."""
        self._check_catalog()
        field = dao.Asset.import_session
        query = self.session.query(field).group_by(field)
        return [s.import_session for s in query.all()]

    def info(self, object, parameter):
        """Get information about an object, given its identifier."""
        self._check_catalog()
        objects = {
            "session": self.__info_session,
            "asset": self.__info_asset
        }
        fn = objects.get(object, None)
        if fn is None:
            raise Exception("Invalid object: %s." % object)
        return fn(parameter)

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
        self._check_catalog()
        functions = {
            'flag': dao.Image.set_flag,
            'label': dao.Image.set_label,
            'rating': dao.Image.set_rating,
            'iptc': dao.Image.set_iptc,
        }
        try:
            for asset in assets:
                q = self.session.query(dao.Image)\
                                .filter(dao.Image.asset_id == asset)
                for image in q:
                    attributes = {key: options[key] for key in functions
                                  if key in options}
                    for attribute, value in attributes.items():
                        fn = functions.get(attribute, None)
                        if fn is None:
                            raise Exception("Invalid attribute %s" % attribute)
                        fn(image, value)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            # TODO: Handle errors.
            raise e
