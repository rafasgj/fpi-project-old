"""Steps to test managing image attributes."""

from behave import when, then

import dao


def _get_image_from_catalog(catalog, asset, image):
    img = int(image.strip()) - 1
    ast = catalog.info('asset', asset)
    return None if ast is None else ast.virtual_copies[img]


@when('setting the flag of {image} of {asset} to {flag}')
def when_setting_image_flag(context, asset, image, flag):
    """Set image flag to the given value."""
    if flag.strip().lower() == 'pick':
        f = dao.Image.Flags.PICK
    elif flag.strip().lower() == 'reject':
        f = dao.Image.Flags.REJECT
    else:
        f = dao.Image.Flags.UNFLAG

    context.command = 'attrib'
    context.options = {'flag': f.value}
    context.assets = [asset]
    context.catalog.set_attributes(context.assets, context.options)


@then('the flag of {image} of {asset} to {flag} is set')
def then_flag_is_set_and_no_other_flag(context, image, asset, flag):
    """Check that a specific flag is set."""
    img = _get_image_from_catalog(context.catalog, asset, image)
    assert img is not None
    assert isinstance(img, dao.Image)
    if flag.strip().lower() == 'pick':
        assert img.pick is True
    elif flag.strip().lower() == 'reject':
        assert img.reject is True
    else:
        assert img.unflagged is True
