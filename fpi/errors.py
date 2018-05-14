"""Define exceptions that can raised."""


class InexistentCatalog(Exception):
    """Define an error for unexistent databases."""

    pass


class UnexpectedCatalogVersion(Exception):
    """Define an error for databases that need to be upgraded."""

    pass
