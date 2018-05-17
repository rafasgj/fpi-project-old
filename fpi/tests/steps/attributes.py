"""Steps to test managing image attributes."""

from behave import when, then

import dao


def _get_image_from_catalog(catalog, asset, image):
    img = int(image.strip()) - 1
    ast = catalog.info('asset', asset)
    return None if ast is None else ast.virtual_copies[img]


# Tests for FLAGS.

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


# Tests for LABELS

@when('setting labels to some assets')
def when_setting_labels(context):
    """Set labels to assets in a catalog."""
    try:
        for row in context.table:
            asset = row['asset'].strip()
            options = {'label': row['label'].strip()}
            context.catalog.set_attributes([asset], options)
        context.exception = None
    except Exception as e:
        context.exception = e


@then('the asset "{asset_id}" has the label "{label}"')
def then_asset_has_label(context, asset_id, label):
    """Verify given asset has the given label."""
    asset = context.catalog.info('asset', asset_id)
    assert asset.label == label


@then('the asset "{asset_id}" has no label.')
def then_asset_no_label(context, asset_id):
    """Verify asset has no label."""
    context.execute_steps('then the asset "%s" has the label ""' % asset_id)


@then('there are {count} assets with the label "{label}"')
def then_count_assets_with_label(context, label, count):
    """Verify number of assets with a specific label."""
    msg = 'STEP: Then there are %d assets with the label "%s"'
    raise NotImplementedError(msg % (count, label))


@then('there are {count} assets with no label')
def then_count_assets_no_label(context, count):
    """Verify number of assets with no label."""
    context.execute_steps('there are %d assets with the label ""' % count)
