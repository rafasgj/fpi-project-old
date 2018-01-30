"""Define the data objects used on the system."""

from sqlalchemy import Column, String, Integer

import os
import os.path
import hashlib

from base import Base


class Asset(Base):
    """Models the high level catalog asset."""

    __tablename__ = "assets"
    id = Column(String, primary_key=True)
    original_device_id = Column(Integer)
    original_inode = Column(Integer)
    original_path = Column(String)
    original_filename = Column(String)
    original_size = Column(Integer)
    device_id = Column(Integer)
    path = Column(String)
    filename = Column(String)

    def __init__(self, filepath):
        """Initialize an asset given a path to it."""
        # original file attributes
        st = os.stat(filepath)
        self.original_device_id = st.st_dev
        self.original_inode = st.st_ino
        self.original_size = st.st_size
        dirname, basename = os.path.split(filepath)
        mount = dirname
        while mount != "/":
            if os.path.ismount(mount):
                break
            mount = os.path.dirname(mount)
        self.original_filename = basename
        self.original_path = dirname[len(mount):]
        # asset attributes
        self.device_id = self.original_device_id
        self.path = self.original_path
        self.filename = self.original_filename
        data = '{:04x}'.format(self.original_device_id)
        data += '{:016x}'.format(self.original_inode)
        data += self.original_path.replace('/', '')
        data += self.original_filename
        data += '{:016x}'.format(self.original_size)
        md5hash = hashlib.md5()
        md5hash.update(data.encode('utf-8'))
        self.id = md5hash.hexdigest()
