"""Define the data objects used on the system."""

from sqlalchemy import Column, ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import relationship
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
    type = Column(String)
    device_id = Column(Integer)
    path = Column(String)
    filename = Column(String)
    import_time = Column(DateTime)
    import_session = Column(String)

    virtual_copies = relationship("Image", backref="asset")

    @hybrid_property
    def fullpath(self):
        """Obtain the full path of an asset."""
        return os.path.join(self.path, self.filename)

    @staticmethod
    def __get_mount_point(filepath):
        while len(filepath) > 0:
            if os.path.ismount(filepath):
                return filepath
            filepath = os.path.dirname(filepath)
        return ""

    def __init__(self, filepath, session_name):
        """Initialize an asset given a path to it."""
        # asset attributes
        dirname, basename = os.path.split(filepath)
        dirname = os.path.realpath(dirname)
        st = os.stat(filepath)
        self.device_id = st.st_dev
        self.filename = basename
        mount = Asset.__get_mount_point(dirname)
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


class Image(Base):
    """Models an Image, for the DAM system."""

    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    asset_id = Column(String, ForeignKey('assets.id'))
    capture_datetime = Column(DateTime)
    width = Column(Integer)
    height = Column(Integer)

    # asset = relationship("Asset", back_populates="virtual_copies")

    def __init__(self, asset, filepath):
        """Initialize a new image asset."""
        exif = GExiv2.Metadata(filepath)
        self.capture_datetime = self.__get_capture_datetime(exif)
        self.width = exif.get('Exif.Photo.PixelXDimension')
        self.height = exif.get('Exif.Photo.PixelYDimension')
        self.asset = asset

    def __get_capture_datetime(self, exif):
        capture_tag = ['Exif.Photo.DateTimeOriginal',
                       'Exif.Photo.DateTimeDigitized',
                       'Iptc.Application2.DateCreated',
                       'Iptc.Application2.DigitizationDate',
                       'Exif.Image.DateTime',
                       'Xmp.xmp.CreateDate']
        for tag in capture_tag:
            value = exif.get(tag)
            if value is not None:
                if tag.startswith('Exif.'):
                    fmt = "%Y:%m:%d %H:%M:%S"
                    dt = datetime.datetime.strptime(value, fmt)
                else:    # XMP or IPTC
                    if tag.startswith("Iptc."):
                        if tag.endswith(".DateCreated"):
                            timetag = "Iptc.Application2.TimeCreated"
                        else:
                            timetag = "Iptc.Application2.DigitizationTime"
                        tg = exif.get(timetag)
                        if tg is None:
                            continue
                        value = value + "T" + tg
                    fmt = "%Y-%m-%dT%H:%M:%S"
                    dt = datetime.datetime.strptime(value[:19], fmt)
                return dt
        else:
            raise Exception("Could not retrieve capture_datetime")
