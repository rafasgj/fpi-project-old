"""Define the data objects used on the system."""

from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

import os, os.path
import hashlib
import datetime
import base64
import io

import PIL.Image
from enum import Enum

import phexif

from base import Base


class Metadata(object):
    """Ease EXIF, IPTC and XMP metadata handling."""

    def __init__(self, filepath):
        """Initialize a new metadata object by loading the file metadata."""
        self.filepath = filepath
        with phexif.ExifTool() as et:
            self.info = et.get_metadata(filepath)[0]
        self._capture_datetime = self._extract_datetime()
        self._width, self._height = self._get_dimension()
        self._thumbnail = None

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
        """Return a tumbnail of the image."""
        if self._thumbnail is None:
            self._thumbnail = self._get_thumbnail()
        return self._thumbnail

    def _get_thumbnail(self):
        """Extract the metadata thumbnail."""
        tags = ['EXIF:ThumbnailImage', 'EXIF:PreviewImage']
        for tag in tags:
            t = self.info.get(tag)
            if t is not None:
                return base64.b64decode(t.split(":")[-1])
        img = PIL.Image.open(self.info.get('SourceFile'))
        img.thumbnail((192, 192), PIL.Image.ANTIALIAS)
        barray = io.BytesIO()
        img.save(barray, format="JPEG")
        return barray.getvalue()

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
        capture_tag = ['EXIF:DateTimeOriginal',
                       'EXIF:DateTimeDigitized',
                       'IPTC:DateCreated',
                       'IPTC:DigitizationDate',
                       'EXIF:DateTime',
                       'XMP:CreateDate']
        for tag in capture_tag:
            value = self.info.get(tag)
            if value is not None:
                if tag.startswith("IPTC:"):
                    if tag.endswith("DateCreated"):
                        timetag = "IPTC:TimeCreated"
                    else:
                        timetag = "IPTC:DigitizationTime"
                    tg = self.info.get(timetag)
                    if tg is None:
                        continue
                    value = value + " " + tg
                fmt = "%Y:%m:%d %H:%M:%S"
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

    virtual_copies = relationship("Image", back_populates="asset")

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
        exif = Metadata(filepath)
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
    flag = Column(Integer, nullable=True)
    label = Column(String, nullable=True)
    rating = Column(Integer, nullable=False, server_default='0', default=0)

    asset = relationship("Asset", back_populates="virtual_copies")
    iptc = relationship("ImageIPTC", back_populates="image", uselist=False)

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

    # The use of set_<attribute> makes it easier to implement a
    # generic set_attribute method in the Catalog.

    def set_flag(self, _, value):
        """Set flag for this object."""
        if value in Image.Flags:
            value = value.value
        if Image.Flags(value) not in Image.Flags:
            raise Exception("Internal Error: Invalid flag value")
        if value != self.flag:
                self.flag = value

    def set_label(self, _, value):
        """Set the label attribute."""
        self.label = value

    def set_rating(self, _, value):
        """Set the label attribute."""
        rating = int(value)
        if 0 <= rating <= 5:
            self.rating = rating
        else:
            raise ValueError("Rating must be in the range [0;5]")

    def set_iptc(self, key, value):
        """Set an iptc/xmp value."""
        self.iptc.set(key, value)

    def __init__(self, asset, metadata):
        """Initialize a new image asset."""
        self.capture_datetime = metadata.capture_datetime
        self.width = metadata.width
        self.height = metadata.height
        self.asset = asset
        self.iptc = ImageIPTC(metadata)


class ImageIPTC(Base):
    """Separate the Caption from the Image table."""

    __tablename__ = "imageIPTC"
    image_id = Column(Integer, ForeignKey('images.id'), primary_key=True)
    caption = Column(Text, nullable=True)
    title = Column(String, nullable=True)
    creator = Column(String, nullable=True)
    jobtitle = Column(String, nullable=True)
    city = Column(String, nullable=True)

    image = relationship("Image", back_populates="iptc", uselist=False)

    iptc_fields = {
        'caption': ['EXIF:ImageDescription', 'XMP:Description',
                    'IPTC:Caption-Abstract'],
        'title': ['XMP:Title', 'IPTC:ObjectName'],
        'creator': ['EXIF:Artist', 'XMP:Creator', 'IPTC:By-line'],
        'jobtitle': ['XMP:AuthorsPosition', 'IPTC:By-lineTitle'],
        'city': ['XMP:City', 'IPTC:City'],
    }

    def __init__(self, metadata):
        """Initialize XMP/IPTC metadata information."""
        for field, tags in ImageIPTC.iptc_fields.items():
            setattr(self, field, self._get_metainfo(metadata, tags))

    def _get_metainfo(self, metadata, tags):
        for t in tags:
            value = metadata.info.get(t)
            if value is not None:
                return value
        else:
            return None

    def set(self, key, value):
        """Set a key/value pair."""
        # This seems wrong, but key is often 'iptc.<fieldname>'.
        field = key.strip().lower().split('.')[-1]
        if hasattr(self, field) is None:
            raise Exception("Invalid or unsupported IPTC/XMP field: %s" % key)
        setattr(self, field, value)
