"""Functions to configure CLI options."""

from optparse import OptionParser, OptionGroup

from cli import configuration


def init(callback=None):
    """Initialize the CLI command parser."""
    desc = """f/π is an open source, catalog-oriented digital asset managemt tool.
            The available commands are: catalog, ingest and info."""
    usage_string = "%prog command catalog [options] file|directory ..."

    opt_parser = OptionParser(usage=usage_string,
                              version="f/π version α-1",
                              description=desc)
    opt_parser.add_option("", "--gui", action="callback", callback=callback,
                          help="start f/π GUI version.")
    return _configure_option_parser(opt_parser)


def _set_method(option, string, parameter, opt_parser):
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
        raise Exception(err % option)


def _init_opt_grp(parser):
    """Initialize the Catalog option group."""
    opt_grp = OptionGroup(parser, "Catalog")
    opt_grp.add_option("", "--new", action="store_true", default=False,
                       help="""creates a new f/π catalog with the given
                               name.""")
    return opt_grp


def _init_ingestion_opt(parser):
    """Initialize the Ingest option group."""
    grp = OptionGroup(parser, "Ingest")
    grp.add_option("", "--add", action="callback",
                   callback=_set_method, nargs=0,
                   help="""ingest files by adding them in their current
                           location.""")
    grp.add_option("", "--copy", action="callback",
                   callback=_set_method, nargs=1, type='string',
                   help="""ingest files by copyng them from their current
                           location to the given directory.""")
    grp.add_option("", "--move", action="callback",
                   callback=_set_method, nargs=1, type='string',
                   help="""ingest files by moving them from their current
                           location to the given directory.""")
    grp.add_option("", "--rename-rule", dest="rename", metavar="RENAME_RULE",
                   help="""describe rename rule.""")
    grp.add_option("", "--directory-rule", dest="directory_rule",
                   help="""describe directory rule.""")
    grp.add_option("", "--recurse", action="store_true", default=False,
                   help="""execute the option recursively starting from the
                           given directory.""")
    grp.add_option("", "--session", dest="session_name",
                   help="""define the import session name.""")
    return grp


def _init_info_opt(parser):
    """Initialize the Info option group."""
    parser = OptionGroup(parser, "Info")
    parser.add_option("", "--list", action="store_true", default=False,
                      help="""list all assets in the catalog or session.""")
    parser.add_option("", "--object", dest="object", default="asset",
                      metavar="TYPE", choices=["session", "asset"],
                      help="""define object type to query. It must be one of
                              asset or session.""")
    parser.add_option("", "--id",
                      help="""the id of the element to query. For session
                              it is the session name. For assets, it is
                              the asset id, and it might be only the initial
                              part of the id.""")
    return parser


def _init_attrib_opt(parser):
    """Initialize the Attrib option group."""
    parser = OptionGroup(parser, "Attrib")
    parser.add_option("-f", "--flag", dest="flag",
                      metavar="FLAG", choices=['pick', 'reject', 'unflag'],
                      help="""Define or remove an asset flag.""")
    return parser


def _configure_option_parser(parser):
    """Configure the option parser with the CLI options."""
    # Add command options
    parser.add_option_group(_init_opt_grp(parser))
    parser.add_option_group(_init_ingestion_opt(parser))
    parser.add_option_group(_init_info_opt(parser))
    parser.add_option_group(_init_attrib_opt(parser))
    # Ok, all configuration is done.
    return parser
