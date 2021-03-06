"""Steps for keywords scenarios."""

from behave import given, when, then

import dao


# CREATE keywords

@given('the keyword "{keyword}" for language "{lang}"')
def given_a_keyword(context, keyword, lang):
    """Set a keyword for a specific language."""
    context.keywords = [keyword]
    context.lang = lang


@given('some keywords')
def given_some_keywords(context):
    """Prepare some keywords in the test context."""
    context.keywords = ["a keyword", "another keyword", "lot's of keywords"]
    context.lang = ''


@when('adding new keywords to the database')
def when_adding_new_keyword_to_the_database(context):
    """Add keywords to the catalog."""
    try:
        context.catalog.add_keywords(context.keywords)
        context.exception = None
    except Exception as e:
        context.exception = e


@then('the keyword "{keyword}" exists in the database')
def then_keyword_exists(context, keyword):
    """Test if the given keyword exists in the database."""
    query = context.catalog.session.query(dao.Keyword)
    query = query.filter(dao.Keyword.text == keyword)
    kw = query.one_or_none()
    assert kw is not None
    observed = kw.text
    assert observed == keyword


@then('each keyword is a public keyword')
def then_keyword_is_public(context):
    """Test if keyword is to be exported."""
    query = context.catalog.session.query(dao.Keyword)
    keys = sum([k.strip().split(':') for k in context.keywords], [])
    query = query.filter(dao.Keyword.text.in_(keys))
    keywords = query.all()
    assert keywords is not None
    for kw in keywords:
        assert kw.private is False
        assert kw.person is False


@then('each keyword can have synonyms exported')
def then_keyword_export_synonyms(context):
    """Test if keyword synonyms are to be exported."""
    query = context.catalog.session.query(dao.Keyword)
    keys = sum([k.strip().split(':') for k in context.keywords], [])
    query = query.filter(dao.Keyword.text.in_(keys))
    keywords = query.all()
    assert keywords is not None
    for kw in keywords:
        assert kw.export_synonyms is True


@then('each keyword has {count:d} synonyms')
def then_keyword_has_no_synonyms(context, count):
    """Test if the keyword has the right number of synonyms."""
    query = context.catalog.session.query(dao.Keyword)
    keys = sum([k.strip().split(':') for k in context.keywords], [])
    query = query.filter(dao.Keyword.text.in_(keys))
    keywords = query.all()
    assert keywords is not None
    for kw in keywords:
        assert len(kw.synonyms) == count


@then('the keywords exist in the database')
def then_keywords_exist(context):
    """Test if all keywods were correctly added to the database."""
    query = context.catalog.session.query(dao.Keyword)
    keys = sum([k.strip().split(':') for k in context.keywords], [])
    query = query.filter(dao.Keyword.text.in_(keys))
    keywords = query.all()
    assert keywords is not None
    assert len(keywords) == len(context.keywords)
    for kw in keywords:
        assert kw.text in context.keywords


@then('the keyword "{parent}" is parent of "{child}"')
def then_keyword_is_parent_of_another(context, parent, child):
    """Test keyword hierarchy."""
    query = context.catalog.session.query(dao.Keyword)
    parent = query.filter(dao.Keyword.text == parent.strip()).one_or_none()
    child = query.filter(dao.Keyword.text == child.strip()).one_or_none()
    assert parent is not None
    assert child is not None
    assert child.parent is not None
    assert child.parent == parent


@then('the keyword "{parent}" is not parent of "{child}"')
def then_keyword_is_not_parent_of_another(context, parent, child):
    """Test keyword hierarchy."""
    query = context.catalog.session.query(dao.Keyword)
    parent = query.filter(dao.Keyword.text == parent.strip()).one_or_none()
    child = query.filter(dao.Keyword.text == child.strip()).one_or_none()
    assert parent is not None
    assert child is not None
    if child.parent is not None:
        assert child.parent != parent


# ASSIGN Keywords to assets

@given('the keyword "{keyword}" exists in the database')
def given_keyword_exist_in_database(context, keyword):
    """Keyword exists in the database"""
    context.catalog.add_keywords([keyword])


@when('assigning the keyword "{keyword}" to the asset "{asset}"')
def when_assigning_keyword_to_asset(context, keyword, asset):
    """Assign keyword to asset."""
    try:
        context.catalog.apply_keywords([asset], [keyword])
    except Exception as e:
        context.exception = e


@when('removing keyword "{keyword}" from asset "{asset}"')
def when_removing_keyword_from_asset(context, keyword, asset):
    """Remove a keyword from an asset."""
    try:
        context.catalog.remove_keywords([asset], [keyword])
    except Exception as e:
        context.exception = e


@then('the asset "{asset}" has the keyword "{keyword}"')
def then_asset_has_keyword(context, asset, keyword):
    """Check if asset has the keyword."""
    asset = context.catalog.info('asset', asset)
    keywords = [k.text for k in asset.virtual_copies[0].keywords]
    assert keyword in keywords


# REMOVE keywords

@given('the keyword "{keyword}" is assigned to asset "{asset}"')
def given_asset_has_keyword_assigned(context, keyword, asset):
    """Assign keyword to asset."""
    context.catalog.apply_keywords([asset], [keyword])


@when('removing the keyword "{keyword}"')
def when_removing_keyword(context, keyword):
    """Delete keyword from the database."""
    try:
        context.catalog.delete_keyword(keyword)
        context.exception = None
    except Exception as e:
        context.exception = e


@when('forcing removal of the keyword "{keyword}"')
def when_force_removal_of_keyword(context, keyword):
    """Force removal of a keyword from the database."""
    try:
        context.catalog.delete_keyword(keyword, force=True)
        context.exception = None
    except Exception as e:
        context.exception = e


@then('the keyword "{keyword}" does not exist in the database')
def then_keyword_does_not_exist(context, keyword):
    """Check keyword is not in the database."""
    query = context.catalog.session.query(dao.Keyword)
    kw = query.filter(dao.Keyword.text == keyword.strip()).one_or_none()
    assert kw is None


@then('the keyword "{keyword}" has {count:d} children')
def then_keyword_has_some_children(context, keyword, count):
    """Count keyword children."""
    query = context.catalog.session.query(dao.Keyword)
    kw = query.filter(dao.Keyword.text == keyword.strip()).one_or_none()
    assert kw is not None
    assert len(kw.children) == 0


@then('the asset "{asset}" has {count:d} keywords')
def then_asset_has_some_keywords(context, asset, count):
    """Assert asset has the right number of keywords."""
    asset = context.catalog.info('asset', asset)
    assert len(asset.virtual_copies[0].keywords) == count
