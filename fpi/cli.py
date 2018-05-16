"""Configure and run optparse to set configuration based on user options."""

import catalog
import dao


# Processing Options:
#   * Ingest
#   - session_name
#   - target_dir
#   - rename
#   - directory_rule
#   - recurse
#   - method
#   * Attrib
#   - flag
configuration = {}


def process_catalog_cmd(catalog, options, files):
    """Process the CATALOG command."""
    if options.new:
        if len(files) > 0:
            err = """Only the catalog name should be used with --new."""
            raise Exception(err)
        print("Creating catalog.")
        catalog.create()
    if options.upgrade:
        print("Upgrading catalog.")
        catalog.upgrade()
    else:
        raise Exception("Invalid command option.")


def process_ingest_cmd(catalog, options, files):
    """Process the INGEST command."""
    catalog.open()
    configuration['session_name'] = options.session_name
    configuration['rename'] = options.rename
    configuration['directory_rule'] = options.directory_rule
    configuration['recurse'] = options.recurse
    method = configuration.get('method', 'add')
    del(configuration['method'])
    catalog.ingest(method, files, **configuration)


def process_info_cmd(catalog, options, files):
    """Process the INFO command."""
    catalog.open()
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
        _cmd_info_display_asset(catalog, obj, options.id.strip())


def _cmd_info_display_asset(catalog, obj, obj_id):
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


def process_attrib_cmd(catalog, options, assets):
    """Process the ATTRIB command."""
    catalog.open()
    flag_options = {
        'pick': dao.Image.Flags.PICK,
        'reject': dao.Image.Flags.REJECT,
        'unflag': dao.Image.Flags.UNFLAG,
    }
    configuration['flag'] = flag_options.get(options.flag, None)
    catalog.set_attributes(assets, configuration)


commands = {
    'catalog': process_catalog_cmd,
    'ingest': process_ingest_cmd,
    'info': process_info_cmd,
    'attrib': process_attrib_cmd
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
