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


commands = {
    "catalog": process_catalog_cmd,
    "ingest": process_ingest_cmd
}


def execute(options, args):
    """Execute f/π command line interface."""
    command = args[0]
    cat = catalog.Catalog(args[1])
    values = args[2:]

    fn = commands.get(command, None)

    if fn is None:
        raise Exception("Provided command is invalid.")
    else:
        fn(cat, options, values)
