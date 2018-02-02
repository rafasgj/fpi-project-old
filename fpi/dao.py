"""Define the data objects used on the system."""

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.hybrid import hybrid_property

import os, os.path
import hashlib
import datetime

import gobject_import   # noqa: F401
from gi.repository import GExiv2

from base import Base


class Asset(Base):
    """Models the high level catalog asset."""

    __tablename__ = "assets"
    id = Column(String, primary_key=True)
    device_id = Column(Integer)
    path = Column(String)
    filename = Column(String)
    import_time = Column(DateTime)
    import_session = Column(String)

    @hybrid_property
    def fullpath(self):
        """Obtain the full path of an asset."""
        return os.path.join(self.path, self.filename)

    def __get_mount_point(self, dirname):
        while dirname != "/":
            if os.path.ismount(dirname):
                break
            dirname = os.path.dirname(dirname)
        return dirname

    def __init__(self, filepath, session_name):
        """Initialize an asset given a path to it."""
        # asset attributes
        dirname, basename = os.path.split(filepath)
        st = os.stat(filepath)
        self.device_id = st.st_dev
        self.filename = basename
        mount = self.__get_mount_point(dirname)
        self.path = dirname[len(mount):]
        # asset id
        exif = GExiv2.Metadata(filepath)
        thumbnail = exif.get_exif_thumbnail()
        md5hash = hashlib.md5()
        md5hash.update(thumbnail)
        self.id = md5hash.hexdigest()
        # import data
        self.import_time = datetime.datetime.now()
        self.import_session = session_name
