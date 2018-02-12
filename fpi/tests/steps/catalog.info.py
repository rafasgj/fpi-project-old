"""Steps for the Info command."""

from behave import given, when, then


@given('the command to obtain information about itens in the catalog')
def given_command_info(context):
    """Set the command to 'info'."""
    context.command = "info"


@given('the option to obtain information abount a Session')
def given_option_session(context):
    """Set the option to 'option'."""
    context.option = "session"


@given('the session query as "{session_name}"')
def given_session_name(context, session_name):
    """Given the session name."""
    context.parameter = session_name


@when('requesting information about an item in the catalog')
def when_request_info(context):
    """Request info about an item in the catalog."""
    context.result = context.catalog.info(context.option,
                                          context.parameter)


@then('I expect to see the session name')
def then_session_name_is_correct(context):
    """Check if the session name was correctly retrieved."""
    assert context.result.session_name == context.parameter


@then('I expect to see the fullpath of the files and the asset id')
def then_check_session_asset_fullpath_and_id(context):
    """Check asset fullpath and id."""
    assets = [(r['id'], r['fullpath']) for r in context.table]
    assert len(context.result.assets) == len(assets)
    for asset in context.result.assets:
        for obs in assets:
            if asset.fullpath == obs[1]:
                assert asset.id == obs[0]
                break
        else:
            msg = "Asset not validated: (%s,%s)" % asset
            raise Exception(msg)


@given('the option to obtain information about an Asset')
def given_option_asset(context):
    """Set option to Asset."""
    context.option = "asset"


@given(u'the asset id "{asset_id}"')
def given_an_asset_id(context, asset_id):
    """Set the asset id to be used."""
    context.parameter = asset_id


@then('I expect to see the asset fullpath and id')
def then_check_asset_fullpath_and_id(context):
    """Check if the fullpath and id are correct."""
    row = context.table[0]
    assert context.result.id == row['id']
    assert context.result.fullpath == row['fullpath']


@then('the asset image information for Width, Height and Capture Date/Time')
def then_check_asset_image_information(context):
    """Check if the asset image attributes are correct."""
    row = context.table[0]
    assert len(context.result.virtual_copies) == 1
    img = context.result.virtual_copies[0]
    assert img.width == int(row['Width'].strip())
    assert img.height == int(row['Height'].strip())
    dt = img.capture_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # 2011-10-28 12:00:00
    assert dt.startswith("2011-")
    assert dt.startswith("2011-10")
    assert dt.startswith("2011-10-28")
    assert dt.endswith(":00")
    assert dt.endswith(":00:00")
    assert dt.endswith(" 12:00:00")
    assert dt == row['Capture Date Time'].strip()
