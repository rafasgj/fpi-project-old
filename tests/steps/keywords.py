"""Steps for keywords scenarios."""

from behave import given, when, then

import dao


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


@given('the keyword "{keyword}" exists')
def given_a_keyword_exists(context, keyword):
    """Keyword exists in the catalog."""
    context.keywords = [keyword]
    context.lang = ''
    context.catalog.add_keywords(context.keywords)


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
