"""There must be a common declarative base for all SQLAlchemy use."""

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
