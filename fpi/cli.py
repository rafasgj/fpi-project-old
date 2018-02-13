"""Configure and run optparse to set configuration based on user options."""

import catalog


# Processing Options:
#   - session_name
#   - target_dir
#   - rename
#   - directory_rule
#   - source


def process_catalog_cmd(catalogname, options):
    """Process the CATALOG command."""
    if options.new:
        print("Creating catalog %s" % catalogname)
        cat = catalog.Catalog(catalogname)
        cat.create()
        return
    raise Exception("Ivalid command options.")


_VALID_COMMANDS = [
    "catalog",
    "ingest",
    "info"
]


def execute(options, args):
    """Execute f/π command line interface."""
    command = args[0]
    catalog = args[1]

    if command not in _VALID_COMMANDS:
        raise Exception("Provided command is invalid.")

    if command == "catalog":
        process_catalog_cmd(catalog, options)
    elif command == "ingest":
        raise NotImplementedError("Command not implemented.")
    elif command == "info":
        raise NotImplementedError("Command not implemented.")
