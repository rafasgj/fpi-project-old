"""Steps for testing ingestion by file move."""

from behave import given, then

import os.path


@given('the option to move the file to directory "{target_dir}"')
def given_option_move(context, target_dir):
    """Set the option to move files."""
    context.option = "move"
    context.suboptions['target_dir'] = target_dir


@then('the original files do not exist anymore')
def then_originals_do_not_exist(context):
    """Check if the original files do not exist anymore."""
    for f in context.files:
        assert os.path.exists(f) is False
