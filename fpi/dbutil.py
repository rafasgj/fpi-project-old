"""Define utility classes to use with database objects."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()
Session = sessionmaker()
engine = object()


def get_catalog_filename(catalog):
    """Given a catalog name or filename, return the catalog filename."""
    if catalog.endswith('.fipcat'):
        return catalog
    return "%s.fpicat" % (catalog)


def get_catalog_init_string(catalog):
    """Given a catalog name or filename, return the catalog init string."""
    return "sqlite:///%s" % (get_catalog_filename(catalog))


def init(catalog):
    """Initialize and configure several database classes and objects."""
    global engine, Base, Session
    engine = create_engine(get_catalog_init_string(catalog))
    Session.configure(bind=engine)
