"""Define the data objects used on the system."""

from sqlalchemy import Column, ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

import os, os.path
import hashlib
import datetime

import PIL.Image
from enum import Enum

import gobject_import   # noqa: F401
from gi.repository import GExiv2

from base import Base


class Metadata(object):
    """Ease EXIF, IPTC and XMP metadata handling."""

    def __init__(self, filepath):
        """Initialize a new metadata object by loading the file metadata."""
        self.filepath = filepath
        self.info = GExiv2.Metadata(filepath)
        self._capture_datetime = self._extract_datetime()
        self._width, self._height = self._get_dimension()

    @property
    def capture_datetime(self):
        """Return a datetime object with the image create date time."""
        return self._capture_datetime

    @property
    def width(self):
        """Return the width of the original image."""
        return self._width

    @property
    def height(self):
        """Return the height of the original image."""
        return self._height

    @property
    def thumbnail(self):
        """Extract the metadata thumbnail."""
        return self.info.get_exif_thumbnail()

    def _get_value_from_tags(self, tags):
        value = None
        for tag in tags:
            value = self.info.get(tag)
            if value is not None:
                return value
        return None

    def _get_dimension(self):
        width_tags = ['Exif.Image.ImageWidth',
                      'Exif.Photo.PixelXDimension']
        height_tags = ['Exif.Image.ImageLength',
                       'Exif.Photo.PixelYDimension']

        width = self._get_value_from_tags(width_tags)
        height = self._get_value_from_tags(height_tags)

        if width is None or height is None:
            img = PIL.Image.open(self.filepath)
            width, height = img.size

        return (width, height)

    def _extract_datetime(self):
        capture_tag = ['Exif.Photo.DateTimeOriginal',
                       'Exif.Photo.DateTimeDigitized',
                       'Iptc.Application2.DateCreated',
                       'Iptc.Application2.DigitizationDate',
                       'Exif.Image.DateTime',
                       'Xmp.xmp.CreateDate']
        for tag in capture_tag:
            value = self.info.get(tag)
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
                        tg = self.info.get(timetag)
                        if tg is None:
                            continue
                        value = value + "T" + tg
                    fmt = "%Y-%m-%dT%H:%M:%S"
                    dt = datetime.datetime.strptime(value[:19], fmt)
                return dt
        else:
            raise Exception("Could not retrieve capture_datetime")


class Asset(Base):
    """Models the high level catalog asset."""

    __tablename__ = "assets"
    id = Column(String, primary_key=True)
    device_id = Column(Integer, nullable=False)
    path = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    import_time = Column(DateTime, nullable=False)
    import_session = Column(String, nullable=False)

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

    def __init__(self, filepath, session_name, exif):
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
        thumbnail = exif.thumbnail
        md5hash = hashlib.md5()
        md5hash.update(thumbnail)
        self.id = md5hash.hexdigest()
        # import data
        self.import_time = datetime.datetime.now()
        self.import_session = session_name


class Image(Base):
    """Models an Image, for the DAM system."""

    # Flags
    class Flags(Enum):
        """Define the available Flags for an Image."""

        UNFLAG = 0
        PICK = 1
        REJECT = 2

    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    asset_id = Column(String, ForeignKey('assets.id'))
    capture_datetime = Column(DateTime, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    flag = Column(Integer, nullable=False, default=0)

    # asset = relationship("Asset", back_populates="virtual_copies")

    @hybrid_property
    def pick(self):
        """Return True if the image is flagged as PICK."""
        return self.flag == Image.Flags.PICK.value

    @hybrid_property
    def reject(self):
        """Return True if the image is flagged as REJECT."""
        return self.flag == Image.Flags.REJECT.value

    @hybrid_property
    def unflagged(self):
        """Return True if the image is not flagged."""
        return not (self.pick or self.reject)

    @pick.setter
    def pick(self, value):
        """Set/unset the PICK flag."""
        self.set_flag(Image.Flags.PICK if value is True
                      else Image.Flags.UNFLAG)

    @reject.setter
    def reject(self, value):
        """Set/unset the PICK flag."""
        self.set_flag(Image.FlagsREJECT if value is True
                      else Image.Flags.UNFLAG)

    @unflagged.setter
    def unflagged(self, value):
        """Unflag the object."""
        if value is True:
            self.set_flag(Image.Flags.UNFLAG)

    def set_flag(self, value):
        """Set flag for this object."""
        if value in Image.Flags:
            value = value.value
        if Image.Flags(value) not in Image.Flags:
            raise Exception("Internal Error: Invalid flag value")
        if value != self.flag:
                self.flag = value

    def __init__(self, asset, metadata):
        """Initialize a new image asset."""
        self.capture_datetime = metadata.capture_datetime
        self.width = metadata.width
        self.height = metadata.height
        self.asset = asset
