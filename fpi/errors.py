"""Define exceptions that can raised."""


class InexistentObject(Exception):
    """Define an error for unexistent objects in the database."""

    pass


class InexistentCatalog(Exception):
    """Define an error for unexistent databases."""

    pass


class UnexpectedCatalogVersion(Exception):
    """Define an error for databases that need to be upgraded."""

    pass


class InvalidCommand(Exception):
    """Define an error for invalid commands or options."""

    pass


class RemoveException(Exception):
    """
    Define an error for when it is impossible to remove itens from the
    database.
    """

    pass
