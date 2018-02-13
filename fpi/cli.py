"""Configure and run optparse to set configuration based on user options."""

from optparse import OptionGroup

import catalog


def init_catalog_opt(parser):
    """Initialize the Catalog option group."""
    catalog_opt = OptionGroup(parser, "Catalog")
    catalog_opt.add_option("", "--new", action="store_true", default=False,
                           help="""creates a new f/π catalog with the given
                                   name.""")
    return catalog_opt


def init_ingestion_opt(parser):
    """Initialize the Inges option group."""
    catalog_opt = OptionGroup(parser, "Ingest")
    catalog_opt.add_option("", "--add", action="store_true", default=False,
                           help="""ingest files by adding them in their current
                                   location.""")
    catalog_opt.add_option("", "--copy", dest="target_dir",
                           help="""ingest files by copyng them from their
                                   current location to the given directory.""")
    catalog_opt.add_option("", "--move", dest="target_dir",
                           help="""ingest files by moving them from their
                                   current location to the given directory.""")
    catalog_opt.add_option("", "--rename-rule", dest="rename",
                           help="""describe rename rule.""")
    catalog_opt.add_option("", "--directory-rule",
                           help="""describe directory rule.""")
    catalog_opt.add_option("", "--recurse", action="store_true", default=False,
                           help="""execute the option recursively starting from
                                   the given directory.""")
    return catalog_opt


def init_info_opt(parser):
    """Initialize the Inges option group."""
    parser = OptionGroup(parser, "Info")
    parser.add_option("", "--session", action="store_true", default=False,
                      help="""request information about sessions stored
                              in the catalog.""")
    parser.add_option("", "--file", action="store_true", default=False,
                      help="""request information about an asset file
                              stored in the catalog.""")
    parser.add_option("", "--asset", action="store_true", default=False,
                      help="""request information about an asset stored
                              in the catalog.""")
    parser.add_option("", "--list", action="store_true", default=False,
                      help="""list all assets in the catalog or
                              session.""")
    parser.add_option("", "--id",
                      help="""the id of the element to query. For session
                              it is the session name. For assets, it is
                              the asset id, and it might be only the initial
                              part of the id.""")
    return parser


def configure_option_parser(parser):
    """Configure the option parser with the CLI options."""
    # Add command options
    parser.add_option_group(init_catalog_opt(parser))
    parser.add_option_group(init_ingestion_opt(parser))
    parser.add_option_group(init_info_opt(parser))
    # Ok, all configuration is done.
    return parser


def process_catalog_cmd(catalogname, options):
    """Process the CATALOG command."""
    if options.new:
        print("Creating catalog %s" % catalogname)
        cat = catalog.Catalog(catalogname)
        cat.create()
        return
    raise Exception("Ivalid command options.")


VALID_COMMANDS = [
    "catalog",
    "ingest",
    "info"
]


def execute(options, args):
    """Execute f/π command line interface."""
    command = args[0]
    catalog = args[1]

    if command not in VALID_COMMANDS:
        raise Exception("Provided command is invalid.")

    if command == "catalog":
        process_catalog_cmd(catalog, options)
    elif command == "ingest":
        raise NotImplementedError("Command not implemented.")
    elif command == "info":
        raise NotImplementedError("Command not implemented.")
