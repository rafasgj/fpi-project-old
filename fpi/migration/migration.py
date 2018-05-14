"""Perform database migrations."""

import argparse
import alembic.config
import alembic.command
from alembic.migration import MigrationContext
from sqlalchemy import create_engine

import sys


VERSION = "α-2"
DB_VERSION = {
    None: "no-db",
    "81f865635e09": "α-1",
    "1b68ca65442c": "α-2"
}


def current_version(path_to_db):
    """Retrieve the catalog's current revision."""
    engine = create_engine("sqlite:///%s" % (path_to_db))
    context = MigrationContext.configure(engine.connect())
    revision = context.get_current_revision()
    return revision


def upgrade(path_to_db):
    """Upgrade catalog to current version."""
    # args = [
    #     "--raiseerr",
    #     "-c", "fpi.ini",
    #     "-x", "catalog=%s" % (path_to_db),
    #     "upgrade", "head"
    # ]
    # alembic.config.main(argv=args)
    alembic_cfg = alembic.config.Config('fpi.ini')
    alembic_cfg.cmd_opts = argparse.Namespace()
    setattr(alembic_cfg.cmd_opts, 'x', [])
    alembic_cfg.cmd_opts.x.append("catalog=" + path_to_db)
    alembic.command.upgrade(alembic_cfg, "head")


db = sys.argv[1]
print("f/π version:", DB_VERSION[current_version(db)])
upgrade(db)
print("f/π version:", DB_VERSION[current_version(db)])
