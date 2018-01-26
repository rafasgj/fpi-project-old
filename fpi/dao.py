"""Define the data objects used on the system."""

from sqlalchemy import Column, String

import catalog


class Asset(catalog.Base):
    """Models the high level catalog asset."""

    __tablename__ = "assets"
    id = Column(String, primary_key=True)
    filename = Column(String)
