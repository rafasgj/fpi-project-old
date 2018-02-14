"""Steps for the list command."""

from behave import given, when, then


@given('the command to list assets in the catalog')
def given_command_list(context):
    """Set command to 'list'."""
    context.command = 'list'


@given('the catalog has some assets')
def given_filename_list(context):
    """Add given filenames to the catalog."""
    context.files = [row['filename'] for row in context.table]
    context.catalog.ingest("add", context.files)


@when('listing all assets in the catalog')
def when_listing_assets(context):
    """List all the assets in the catalog."""
    try:
        context.result = context.catalog.search()
        context.exception = None
    except Exception as e:
        context.exception = e


@then('I expect all the assets to be listed, with their id and full path')
def then_compare_filenames_and_ids(context):
    """Compare filename/id obtained with expected ones."""
    for row in context.table:
        for asset in context.result:
            if asset.fullpath == row['fullpath']:
                assert asset.id is row['id']
                break


@given('the catalog has some assets ingested in a session "{session_name}"')
def given_assets_ingested_is_session(context, session_name):
    """Ensure assets were ingested in a specific session."""
    context.files = [row['filename'] for row in context.table]
    context.catalog.ingest("add", context.files, session_name=session_name)


@when('listing all sessions in the catalog')
def when_list_sessions(context):
    """Retrieve all sessions in the catalog."""
    context.result = context.catalog.sessions()


@then('I expect all the session names to be listed')
def then_compare_session_names(context):
    """Check if all expected sessions are listed."""
    sessions = [row['session'].strip() for row in context.table]
    for s in context.result:
        assert s in sessions


@then('I expect the session names to be unique')
def then_session_names_are_unique(context):
    """Check if no session name is repeated."""
    i = 0
    while i < len(context.result) - 1:
        assert context.result[i] not in context.result[i + 1:]
        i += 1
