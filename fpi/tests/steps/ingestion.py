"""Basic ingestion steps."""

from behave import given, when, then

import os.path
import datetime

from dao import Asset


# When testing ingestion, the following options are available.
#    - context.ingest_method: {add, copy, move}
#    - context.files: a list of files to ingest.
#    - context.suboptions: A dictionaire with the ingest options
#        - session_name: The session name (string, optional)
#           * "Given a session name of {session_name}"
#        - recurse: To recurse subdirectiories (boolean, optional, True)
#           * "Given the option to ingest recursively"
#        - target_dir: The target directory.  (string, optional)
#           * "Given the target directory {target_dir}"
#        - directory_rule: The rule to create directories. (string, optional)
#           * "Given the directory rule {directory_rule}"


@given('the command to ingest assets')
def given_command_ingest(context):
    """Set command to ingest assets into a catalog."""
    context.command = 'ingest'
    context.ingest_method = 'add'
    context.files = []
    context.suboptions = {}
    now = datetime.datetime.utcnow()
    context.suboptions['session_name'] = now.strftime("%Y-%m-%dT%H:%M:%S.%f%z")


# Ingestion method

@given('the option to add a new file at its position')
def given_option_add(context):
    """Prepare context for creating a new catalog."""
    context.ingest_method = 'add'
    context.suboptions['target_dir'] = None


@given('the option to ingest by copy')
def given_option_copy(context):
    """Set option to copy files during igestion."""
    context.ingest_method = "copy"


@given('the option to ingest by move')
def given_option_move(context):
    """Set the option to move files."""
    context.ingest_method = "move"


@given('the ingestion method {method}')
def given_ingest_method(context, method):
    """Set the ingest method to use."""
    context.ingest_method = method


# Directory options

@given('the target directory "{target_dir}"')
def given_target_directory(context, target_dir):
    """Set target directory option."""
    context.suboptions['target_dir'] = target_dir


@given('the source directory "{sourcedir}"')
def given_source_directory(context, sourcedir):
    """Set the directory to ingest from."""
    context.files = [sourcedir]


@given('the option to ingest recursively')
def given_suboption_recurse(context):
    """Set the option to recursively ingest directories."""
    context.suboptions['recurse'] = True


@given('the directory rule "{directory_rule}"')
def step_impl(context, directory_rule):
    """Set the directory creation rule."""
    context.suboptions['directory_rule'] = directory_rule


# Set rename rule

@given('the rename rule "{rename_rule}"')
def given_rename_rule(context, rename_rule):
    """Set option to rename files."""
    context.suboptions['rename'] = rename_rule


# Files to ingest

@given('an image file at "{imagefile}"')
def given_path_to_image_file(context, imagefile):
    """Prepare context for ingesting an image."""
    assert os.path.isfile(imagefile) is True
    context.files = [imagefile]


@given('a list of files')
def given_list_of_files(context):
    """Set list of files to be ingested."""
    context.files = [row['filename'] for row in context.table]


@given('an image without an embedded thumbnail "{filename}"')
def given_image_without_thumbnail(context, filename):
    """Set an image to be ingested that do not hav an embedded thumbnail."""
    context.files = [filename]


# Session name

@given('a session name of "{session_name}"')
def given_session_name(context, session_name):
    """Set the name of the current import session."""
    context.suboptions['session_name'] = session_name


# Do ingestion.

@when('ingesting assets into the catalog')
def when_ingesting_assets(context):
    """Ingest a file into the catalog and keep it where it is."""
    try:
        context.catalog.ingest(
            context.ingest_method,
            context.files,
            **context.suboptions)
        context.exception = None
    except Exception as e:
        context.exception = e


# Count attributes ingested

@then('one asset is in the catalog with its attributes')
def then_one_asset_is_in_the_catalog(context):
    """Check if the asset was correctly stored in the catalog."""
    assert context.session.query(Asset).count() is 1


@then('there are {some} assets is the catalog, with its attributes')
def then_some_assets_are_stored(context, some):
    """Check if the right number of assets were added to the catalog."""
    count = context.session.query(Asset).count()
    if count != int(some):
        fmt = "Number of objects do not match: %d != %d."
        msg = fmt % (count, int(some))
        raise Exception(msg)


# Test asset attributes.

@then('the destination file attributes are stored within the asset')
def then_asset_destination_file_attributes_are_stored(context):
    """Check if the destination file attributes were correctly saved."""
    for device_id, filename, path in context.table:
        filename = filename.strip()
        query = context.session.query(Asset)
        asset = query.filter(Asset.filename == filename).one()
        assert asset.device_id == int(device_id.strip())
        # assert asset.device_label == device_id
        assert asset.filename == filename
        assert asset.path == path.strip()


@then('the asset id is the MD5 hash "{hashvalue}"')
def then_asset_id_is_md5_hash(context, hashvalue):
    """Check if th asset id was correctly obtained."""
    asset = context.session.query(Asset).one()
    assert asset.id == hashvalue.strip()


@then('the assets id is a MD5 hash')
def then_check_assets_id_hash(context):
    """Check if th assets id was correctly obtained."""
    for filename, md5 in context.table:
        query = context.session.query(Asset)
        asset = query.filter(Asset.filename == filename.strip()).one()
        assert asset.id == md5.strip()


# Limit ingestion time.

@then('its import time is within {some} seconds from the current time')
def then_check_import_time(context, some):
    """Check if the import procedure was efficent enough."""
    query = context.session.query(Asset)
    basename = os.path.basename(context.files[0])
    asset = query.filter(Asset.filename == basename).one()
    now = datetime.datetime.now()
    assert asset.import_time <= now
    assert (now - asset.import_time).total_seconds() < int(some.strip())


# Session tests.

@then('the import session title is the UTC time when the scenario started')
def then_check_import_session_default(context):
    """Check if the import session name matches the default session name."""
    query = context.session.query(Asset)
    basename = os.path.basename(context.files[0])
    asset = query.filter(Asset.filename == basename).one()
    assert asset.import_session == context.suboptions.get('session_name', None)


@then('the import session title is "{session_name}"')
def then_check_session_name(context, session_name):
    """Verify if the session name was correctly configured."""
    query = context.session.query(Asset)
    basename = os.path.basename(context.files[0])
    asset = query.filter(Asset.filename == basename).one()
    assert asset.import_session == context.suboptions.get('session_name', None)


# File location.

@then('the original files are in their original places')
def then_original_files_exist(context):
    """Ensure all original files still exist in their original places."""
    for f in context.files:
        assert os.path.isfile(f) is True


@then('the destination files are in their respective places')
def then_files_are_in_their_correct_places(context):
    """Check if the destination files are in the correct place."""
    for f in [row['filename'] for row in context.table]:
        assert os.path.isfile(f) is True


@then('the original files do not exist anymore')
def then_originals_do_not_exist(context):
    """Check if the original files do not exist anymore."""
    for f in context.files:
        if os.path.exists(f):
            if os.path.isfile(f):
                raise Exception("File exists: %s" % f)
