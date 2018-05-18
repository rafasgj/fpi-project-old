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
#   - label
configuration = {}


def _open_catalog(options):
    cat = catalog.Catalog(options.catalog[0])
    cat.open()
    return cat


def process_catalog_cmd(options):
    """Process the CATALOG command."""
    if options.new is not None:
        print("Creating catalog.")
        catalog.Catalog(options.new).create()
    elif options.upgrade is not None:
        print("Upgrading catalog.")
        catalog.Catalog(options.upgrade).upgrade()
    else:
        raise Exception("Invalid command option.")


def process_ingest_cmd(options):
    """Process the INGEST command."""
    files = options.file
    cat = _open_catalog(options)
    configuration['session_name'] = options.session_name
    configuration['rename'] = options.rename
    configuration['directory_rule'] = options.directory_rule
    configuration['recurse'] = options.recurse
    method = configuration.get('method', 'add')
    del(configuration['method'])
    cat.ingest(method, files, **configuration)


def process_info_cmd(options):
    """Process the INFO command."""
    cat = _open_catalog(options)
    obj = options.object.strip().lower() \
        if options.object is not None else None

    if options.list:
        if obj == 'session':
            for session in cat.sessions():
                print(session)
        else:
            for asset in cat.search():
                print('id: %s\tfile: @%s' % (asset.id, asset.fullpath))
    else:
        if options.id is None:
            raise Exception("Asset ID is necessary.")
        _cmd_info_display_asset(cat, obj, options.id.strip())


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
                \n\theight: {height}\n\tcapture time: {capture}\n"
        print(fmt.format(**info))


def process_attrib_cmd(options):
    """Process the ATTRIB command."""
    def add_attribute(key, value):
        if value is not None:
            configuration[key] = value

    assets = options.asset_id
    cat = _open_catalog(options)

    flag_options = {
        'pick': dao.Image.Flags.PICK,
        'reject': dao.Image.Flags.REJECT,
        'unflag': dao.Image.Flags.UNFLAG,
    }
    # flag attribute
    flag = flag_options.get(options.flag, None)
    add_attribute('flag', flag)
    # label attribute
    add_attribute('label', options.label)
    # rating attribute
    add_attribute('rating', int(options.rating))
    # add attributes to assets.
    cat.set_attributes(assets, configuration)


commands = {
    'catalog': process_catalog_cmd,
    'ingest': process_ingest_cmd,
    'info': process_info_cmd,
    'attrib': process_attrib_cmd
}


def execute(args):
    """Execute f/π command line interface."""
    fn = commands.get(args.command, None)
    if fn is None:
        raise Exception("Provided command is invalid.")
    else:
        fn(args)
