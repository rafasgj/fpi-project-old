"""Define the data objects used on the system."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

from dbutil import Base


class Asset(Base):
    """Models the high level catalog asset."""

    __tablename__ = "assets"
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    disk_label = Column(String)
    path = Column(String)
