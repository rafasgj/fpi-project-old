"""Steps for the list command."""

from behave import given, when, then
import dao

import datetime


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
        context.catalog.open()
        context.result = context.catalog.search()
        context.exception = None
    except Exception as e:
        context.exception = e


@then('I expect {count} assets to be listed, with their id and full path')
def then_compare_filenames_and_ids(context, count):
    """Compare filename/id obtained with expected ones."""
    assert len(context.result) == int(count)
    for row in context.table:
        for image in context.result:
            if image.asset.fullpath == row['fullpath']:
                assert image.asset.id == row['id']
                break
        else:
            raise Exception("No asset matches %s" % row['fullpath'])


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


# Filter catalog
def _filter_catalog(context, options):
    try:
        context.catalog.open()
        context.result = context.catalog.search(options)
        context.exception = None
    except Exception as e:
        context.exception = e


# Filter by FLAG

@given('some images have the flag attribute set to "{flag}"')
def given_some_images_have_flags(context, flag):
    """Set flags of some assets."""
    f = {
        'pick': dao.Image.Flags.PICK,
        'reject': dao.Image.Flags.REJECT
    }.get(flag.strip(), dao.Image.Flags.UNFLAG).value
    options = {'flag': f}
    assets = [row['asset'] for row in context.table]
    context.catalog.set_attributes(assets, options)


@when('listing assets with the flag attribute set to "{flag}"')
def when_listing_assets_based_on_flag(context, flag):
    """List assets with the given flag."""
    f = {
        'pick': dao.Image.Flags.PICK,
        'reject': dao.Image.Flags.REJECT
    }.get(flag.strip(), dao.Image.Flags.UNFLAG).value
    _filter_catalog(context, {'flag': f})


# Filter by LABEL

@given('some images have the label attribute set to "{label}"')
def given_some_images_have_label(context, label):
    """Set the label attribute for some images."""
    options = {'label': label}
    assets = [row['asset'] for row in context.table]
    context.catalog.set_attributes(assets, options)


# Filter by RATING

@given('some images have the rating attribute set to {rating}')
def given_images_have_rating(context, rating):
    """Set image rating to the given value."""
    options = {'rating': int(rating.strip())}
    assets = [row['asset'] for row in context.table]
    context.catalog.set_attributes(assets, options)


@when('listing assets with the rating attribute is "{operator}" {rating}')
def when_listing_assets_based_on_rating(context, operator, rating):
    """List assets based on a rating comparision."""
    operators = {
        "equal to": "==",
        "different than": "!=",
        "less or equal to": "<=",
        "less than": "<",
        "greater or equal to": ">=",
        "greater than": ">="
    }
    query = (operators[operator], rating)
    _filter_catalog(context, {'rating': query})


# Filter by a string field

@when('listing assets with field "{field}", matching partially "{value}"')
def when_filter_strings_matching_partially(context, field, value):
    """List assets based on filename."""
    assert field in ['label', 'filename', 'import_session']
    operation = {
        'partial': True,
        'caseinsensitive': False,
        'not': False
    }
    options = (operation, value)
    _filter_catalog(context, {field: options})


@when('filtering "{field}", with case insensitive partial match to "{value}"')
def when_matching_partially_case_insensitive(context, field, value):
    assert field in ['label', 'filename', 'import_session']
    operation = {
        'partial': True,
        'caseinsensitive': True,
        'not': False
    }
    options = (operation, value)
    _filter_catalog(context, {field: options})


@when('listing assets with field "{field}", matching exactly "{value}"')
def when_filtering_strings_matching_exactly(context, field, value):
    """List assets based on filename."""
    def mapfield(f):
        return "import_session" if f == "session" else f
    assert field in ['label', 'filename', 'session']
    operation = {
        'partial': False,
        'caseinsensitive': False,
        'not': False
    }
    options = (operation, value)
    _filter_catalog(context, {mapfield(field): options})


# Filter by DATE

@when('listing assets with "{datefield}", in the year {year}')
def when_filtering_by_date_year(context, datefield, year):
    """List assetas based on date."""
    year = int(year)
    options = {
        'start': datetime.date(year, 1, 1),
        'end': datetime.date(year, 12, 31)
    }
    _filter_catalog(context, {datefield: options})


@when('listing assets where "{datefield}" is today')
def step_impl(context, datefield):
    """Filter by a date field using current date as parameter."""
    options = {
        'start': datetime.date.today(),
        'end': datetime.date.today()
    }
    _filter_catalog(context, {datefield: options})
