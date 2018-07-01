"""Defines components versions."""

_CURRENT_VERSION = "α-3"


class Version(object):
    """Hold the version values of system components."""

    DB_REVISION = {
        "α-1": "81f865635e09",
        "α-2": "1b68ca65442c",
        "α-3": "a845b60ac452",
    }
    DB_VERSION = {v: k for k, v in DB_REVISION.items()}

    @classmethod
    def version_string(self):
        """Retrieve the system string version."""
        return "f/π version {}".format(_CURRENT_VERSION)

    @classmethod
    def system(self):
        """Retrive f/π current version."""
        return _CURRENT_VERSION

    @classmethod
    def db_revision(self, version=None):
        """Retrieve database revision for a specific version."""
        v = Version.system() if version is None else version
        return Version.DB_REVISION.get(v, "invalid")

    @classmethod
    def db_version(self, revision=None):
        """Retriver the system version for a database revision."""
        v = self.db_revision() if revision is None else revision
        return Version.DB_VERSION.get(v, "invalid")

    @classmethod
    def version_match(self, revision):
        """
        Check if a database revision matches the expected revision for
        current version.
        """
        return Version.db_version(revision) == Version.system()
