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
    else:
        raise Exception("Invalid command option.")


def process_ingest_cmd(catalog, options, files):
    """Process the INGEST command."""
    configuration['session_name'] = options.session_name
    configuration['rename'] = options.rename
    configuration['directory_rule'] = options.directory_rule
    configuration['recurse'] = options.rename if options.rename else False
    method = configuration.get('method', 'add')
    del(configuration['method'])
    catalog.ingest(method, files, **configuration)


def process_info_cmd(catalog, options, files):
    """Process the INFO command."""
    obj = options.object.strip().lower() \
        if options.object is not None else None

    if options.list:
        if obj == 'session':
            for session in catalog.sessions():
                print(session)
        else:
            for asset in catalog.search():
                print('id: %s\tfile: @%s' % (asset.id, asset.fullpath))
    else:
        obj_id = options.id.strip()
        result = catalog.info(obj, obj_id)
        if obj == 'session':
            pass
        else:
            img = result.virtual_copies[0]
            info = {
                "id": result.id,
                "file": result.filename,
                "path": result.path,
                "width": img.width,
                "height": img.height,
                "capture": img.capture_datetime.strftime("%Y-%m-%d %H:%M:%S")
            }
            fmt = "id: {id}\n\tfile: {file}\n\tpath: {path}\n\twidth: {width}\
                   \n\theight: {height}\n\tcapture time:{capture}\n"
            print(fmt.format(**info))


commands = {
    "catalog": process_catalog_cmd,
    "ingest": process_ingest_cmd,
    "info": process_info_cmd
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
