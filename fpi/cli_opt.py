"""Functions to configure CLI options."""

from optparse import OptionGroup


def _init_opt_grp(parser):
    """Initialize the Catalog option group."""
    opt_grp = OptionGroup(parser, "Catalog")
    opt_grp.add_option("", "--new", action="store_true", default=False,
                       help="""creates a new f/π catalog with the given
                               name.""")
    return opt_grp


def _init_ingestion_opt(parser):
    """Initialize the Inges option group."""
    opt_grp = OptionGroup(parser, "Ingest")
    opt_grp.add_option("", "--add", action="store_true", default=False,
                       help="""ingest files by adding them in their current
                               location.""")
    opt_grp.add_option("", "--copy", dest="target_dir",
                       help="""ingest files by copyng them from their
                               current location to the given directory.""")
    opt_grp.add_option("", "--move", dest="target_dir",
                       help="""ingest files by moving them from their
                               current location to the given directory.""")
    opt_grp.add_option("", "--rename-rule", dest="rename",
                       help="""describe rename rule.""")
    opt_grp.add_option("", "--directory-rule",
                       help="""describe directory rule.""")
    opt_grp.add_option("", "--recurse", action="store_true", default=False,
                       help="""execute the option recursively starting from
                               the given directory.""")
    return opt_grp


def _init_info_opt(parser):
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
    parser.add_option_group(_init_opt_grp(parser))
    parser.add_option_group(_init_ingestion_opt(parser))
    parser.add_option_group(_init_info_opt(parser))
    # Ok, all configuration is done.
    return parser
