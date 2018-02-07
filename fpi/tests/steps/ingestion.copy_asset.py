"""Steps for testing ingestion by file copy."""

from behave import given, then

import datetime
import os.path


@given('the option to copy the file to directory "{target_dir}"')
def given_option_copy(context, target_dir):
    """Set option to copy files during igestion."""
    context.option = "copy"
    context.suboptions['target_dir'] = target_dir
    now = datetime.datetime.utcnow()
    context.session_name = now.strftime("%Y-%m-%dT%H:%M:%S.%f%z")


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
