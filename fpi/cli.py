"""Configure and run optparse to set configuration based on user options."""

import catalog


# Processing Options:
#   - session_name
#   - target_dir
#   - rename
#   - directory_rule
#   - recurse
#   - method
configuration = {}


def process_catalog_cmd(catalog, options, files):
    """Process the CATALOG command."""
    if options.new:
        if len(files) > 0:
            err = """Only the catalog name should be used with --new."""
            raise Exception(err)
        print("Creating catalog.")
        catalog.create()
        return
    raise Exception("Ivalid command options.")


def process_ingest_cmd(catalog, options, files):
    """Process the INGEST command."""
    configuration['session_name'] = options.session_name
    configuration['rename'] = options.rename
    configuration['directory_rule'] = options.directory_rule
    configuration['recurse'] = options.rename if options.rename else False
    method = configuration.get('method', 'add')
    del(configuration['method'])
    catalog.ingest(method, files, **configuration)


_VALID_COMMANDS = [
    "catalog",
    "ingest",
    "info"
]


def execute(options, args):
    """Execute f/π command line interface."""
    command = args[0]
    cat = catalog.Catalog(args[1])
    files = args[2:]

    if command not in _VALID_COMMANDS:
        raise Exception("Provided command is invalid.")

    if command == "catalog":
        process_catalog_cmd(cat, options, files)
    elif command == "ingest":
        process_ingest_cmd(cat, options, files)
    elif command == "info":
        raise NotImplementedError("Command not implemented.")
