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
    f = {
        'pick': dao.Image.Flags.PICK,
        'reject': dao.Image.Flags.REJECT
    }.get(flag.strip(), dao.Image.Flags.UNFLAG).value

    context.command = 'attrib'
    context.options = {'flag': f}
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
    assert asset.virtual_copies[0].label == label


@then('the asset "{asset_id}" has no label.')
def then_asset_no_label(context, asset_id):
    """Verify asset has no label."""
    asset = context.catalog.info('asset', asset_id)
    label = asset.virtual_copies[0].label
    assert label in (False, None)


@then('there are {count} assets with the label "{label}"')
def then_count_assets_with_label(context, label, count):
    """Verify number of assets with a specific label."""
    msg = 'STEP: Then there are %d assets with the label "%s"'
    raise NotImplementedError(msg % (count, label))


@then('there are {count} assets with no label')
def then_count_assets_no_label(context, count):
    """Verify number of assets with no label."""
    context.execute_steps('there are %d assets with the label ""' % count)


# Tests for RATINGS

@when('setting ratings to some assets')
def when_setting_ratings(context):
    """Set ratings to assets in a catalog."""
    try:
        for row in context.table:
            asset = row['asset'].strip()
            options = {'rating': row['rating'].strip()}
            context.catalog.set_attributes([asset], options)
        context.exception = None
    except Exception as e:
        context.exception = e


@when(u'setting rating of "{asset_id}" to {rating}')
def when_setting_rating_single_asset(context, asset_id, rating):
    """Set rating of a single asset in a catalog."""
    try:
        context.catalog.set_attributes([asset_id], {'rating': rating})
    except Exception as e:
        context.exception = e


@when('setting the iptc fields of some assets')
def when_setting_iptc_fields(context):
    """Set iptc fields."""
    try:
        for row in context.table:
            asset_id, image, field, value = \
                [row[i].strip() for i in ['asset', 'image', 'field', 'value']]
            field = "iptc.{}".format(field)
            context.catalog.set_attributes([asset_id], {field: value})
    except Exception as e:
        context.exception = e


@when('setting the iptc {field} of asset {asset}/{image} with value {value}')
def when_setting_iptc_fields(context, field, asset, image, value):
    """Set iptc fields."""
    try:
        field = "iptc.{}".format(field)
        context.catalog.set_attributes([asset], {field: value})
    except Exception as e:
        context.exception = e


@then('the asset "{asset_id}" has the rating {rating}')
def then_asset_has_rating(context, asset_id, rating):
    """Verify given asset has the given rating."""
    asset = context.catalog.info('asset', asset_id)
    value = int(rating)
    assert 0 <= value <= 5
    assert asset.virtual_copies[0].rating == value


@then('the asset "{asset_id}" iptc field {field} is "{value}"')
def then_asset_has_iptc_field_with_value(context, asset_id, field, value):
    """Check image IPTC field."""
    asset = context.catalog.info('asset', asset_id)
    assert hasattr(asset.virtual_copies[0].iptc, field) is True
    observed = getattr(asset.virtual_copies[0].iptc, field)
    assert observed == value
