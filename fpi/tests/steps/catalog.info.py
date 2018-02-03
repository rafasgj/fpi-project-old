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


@given('the name of a session as "{session_name}"')
def given_session_name(context, session_name):
    """Given the session name."""
    context.session_name = session_name


@when('requesting information about an item in the catalog')
def when_request_info(context):
    """Request info about an item in the catalog."""
    context.result = context.catalog.info(context.option,
                                          context.session_name)


@then('I expect to see the session name')
def then_session_name_is_correct(context):
    """Check if the session name was correctly retrieved."""
    assert context.result.session_name == context.session_name


@then('I expect to see the fullpath of the files and the asset id')
def then_check_asset_fullpath_and_id(context):
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
