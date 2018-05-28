"""Configure and run optparse to set configuration based on user options."""

import catalog
import dao
import errors

import dateutil.parser
import datetime


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
#   - rating
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
        raise errors.InvalidCommand("Invalid command option.")


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
            searchopt = _process_search_options(options)
            for image in cat.search(searchopt):
                data = (image.asset.id, image.asset.fullpath)
                print('id: %s\tfile: %s' % data)
    else:
        if options.id is None:
            msg = "Session name or Asset ID are necessary."
            raise errors.InvalidCommand(msg)
        _cmd_info_display_asset(cat, obj, options.id.strip())


def _process_search_options(options):
    searchopt = {}
    stropts = {
        'not': options.negate,
        'partial': options.partial,
        'caseinsensitive': not options.exactcase,
    }
    #
    if options.flag:
        searchopt['flag'] = (stropts, options.flag)
    #
    if options.label:
        searchopt['label'] = (stropts, options.label)
    if options.filename:
        searchopt['filename'] = (stropts, options.filename)
    if options.session:
        searchopt['import_session'] = (stropts, options.session)
    #
    searchopt = _process_search_date_options(searchopt, options)
    #
    if options.rating:
        op, value = options.rating
        searchopt['rating'] = (_get_relational_operator(op), value)
    #
    return searchopt


def _process_search_date_options(searchopt, options):
    if options.datefield in ['ingest', 'capture']:
        dateopts = {}
        startdate, enddate = None, None
        #
        default = datetime.datetime(1900, 1, 1, 0, 0, 0)
        startdate = dateutil.parser.parse(options.startdate, default=default)
        #
        current_year = datetime.datetime.today().year
        default = datetime.datetime(current_year, 12, 31, 23, 59, 59)
        enddate = dateutil.parser.parse(options.enddate, default=default)
        #
        dateopts['start'] = startdate
        dateopts['end'] = enddate
        datelabel = {
            'ingest': 'import_date',
            'capture': 'capture_datetime'
        }
        searchopt[datelabel[options.datefield]] = dateopts
    return searchopt


def _get_relational_operator(operator):
    operators = {
        "equal": "==",
        "equal to": "==",
        "different": "!=",
        "different than": "!=",
        "less or equal": "<=",
        "less or equal to": "<=",
        "less": "<",
        "less than": "<",
        "greater or equal": ">=",
        "greater or equal to": ">=",
        "greater": ">=",
        "greater than": ">="
    }
    return operators.get(operator, operator)


def _cmd_info_display_asset(catalog, obj, obj_id):
    result = catalog.info(obj, obj_id)
    if obj == 'session':
        sessionhdr = "Session Name: {session_name}\n" + \
            "Session Start: {creation_time}"
        assetinfo = "id: {id} file: {fullpath}"
        print(sessionhdr.format(**result._asdict()))
        for asset in result.assets:
            print(assetinfo.format(**asset._asdict()))
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
        raise errors.InvalidCommand("Provided command is invalid.")
    else:
        fn(args)
