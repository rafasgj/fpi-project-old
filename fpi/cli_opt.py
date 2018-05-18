"""Functions to configure CLI options."""

# from optparse import OptionParser, OptionGroup
from argparse import ArgumentParser, Action

from cli import configuration


def init():
    """Initialize the CLI command parser."""
    desc = """
           f/π is an open source, catalog-oriented digital asset managemt tool.
           The available commands are: catalog, ingest and info.
           """
    epilog = """
             Check the command options by issuing `fpi <command> --help`
             """
    opt_parser = ArgumentParser(description=desc, epilog=epilog)
    opt_parser.add_argument("--gui", action="store_true",
                            help="start f/π GUI version.")
    opt_parser.add_argument('-v', '--version', action="version",
                            version="f/π version α-1",
                            help="Print f/π version.")
    _configure_option_parser(opt_parser)
    return opt_parser


def _init_opt_grp(parser):
    """Initialize the Catalog option group."""
    opt_grp = parser.add_parser("catalog", help="Manage a catalog.")
    options = opt_grp.add_mutually_exclusive_group(required=True)
    options.add_argument("--new", action="store", metavar="CATALOG",
                         help="""creates a new f/π catalog with the given
                                 name.""")
    options.add_argument("--upgrade", action="store", metavar="CATALOG",
                         help="""upgrades a f/π catalog to the latest
                                 revision.""")


def _init_ingestion_opt(parser):
    """Initialize the Ingest option group."""
    grp = parser.add_parser("ingest", help="Ingest files into the catalog.")
    opt = grp.add_mutually_exclusive_group(required=True)
    opt.add_argument('--add', action=_IngestMethod, nargs=0,
                     help="""ingest files by adding them in their current
                             location.""")
    opt.add_argument('--copy', action=_IngestMethod, metavar="DIRECTORY",
                     dest="target_dir",
                     help="""ingest files by copyng them from their current
                             location to the given directory.""")
    opt.add_argument('--move', action=_IngestMethod, metavar="DIRECTORY",
                     dest="target_dir",
                     help="""ingest files by moving them from their current
                             location to the given directory.""")
    grp.add_argument("--rename-rule", dest="rename", metavar="RENAME_RULE",
                     help="""describe rename rule.""")
    grp.add_argument("--directory-rule", dest="directory_rule",
                     help="""describe directory rule.""")
    grp.add_argument("--recurse", action="store_true", default=False,
                     help="""ingest recursively starting from the given
                             directory.""")
    grp.add_argument("--session", dest="session_name",
                     help="""define the import session name.""")
    grp.add_argument('catalog', nargs=1)
    grp.add_argument('file', nargs='+')


class _IngestMethod(Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(_IngestMethod, self).__init__(option_strings, dest,
                                            nargs, **kwargs)

    def __call__(self, parser, namespace, parameter, string=None):
        if configuration.get('method', None) is not None:
            raise ValueError("Can only set one ingestion method.")
        if string == '--add':
            configuration['method'] = 'add'
            configuration['target_dir'] = None
        elif string == '--copy':
            configuration['method'] = 'copy'
            configuration['target_dir'] = parameter
        elif string == '--move':
            configuration['method'] = 'move'
            configuration['target_dir'] = parameter
        else:
            err = "Internal error: invalid ingestion option '%s'"
            raise Exception(err % string)


def _init_info_opt(parser):
    """Initialize the Info option group."""
    grp = parser.add_parser("info", help="retrieve information abount assets.")
    grp.add_argument("--list", action="store_true", default=False,
                     help="""list all assets in the catalog or session.""")
    grp.add_argument("--object", dest="object", default="asset",
                     choices=["session", "asset"],
                     help="""define object type to query. It must be one of
                             asset or session.""")
    grp.add_argument("--id",
                     help="""the id of the element to query. For session
                             it is the session name. For assets, it is
                             the asset id, and it might be only the initial
                             part of the id.""")
    grp.add_argument('catalog', nargs=1)


def _init_attrib_opt(parser):
    """Initialize the Attrib option group."""
    grp = parser.add_parser("attrib",
                            help="""set attributes for assets.""")
    grp.add_argument("-f", "--flag", dest="flag",
                     choices=['pick', 'reject', 'unflag'],
                     help="""Define or remove a flag attribute.""")
    grp.add_argument("-l", "--label", dest="label",
                     help="""Define a label for an asset.""")
    grp.add_argument('catalog', nargs=1)
    grp.add_argument('asset_id', nargs='+')


def _configure_option_parser(parser):
    """Configure the option parser with the CLI options."""
    subparser = parser.add_subparsers(title="Available commands",
                                      dest='command')
    _init_opt_grp(subparser)
    _init_ingestion_opt(subparser)
    _init_info_opt(subparser)
    _init_attrib_opt(subparser)
