"""Steps for keywords scenarios."""

from behave import given, when, then

import dao


@given('the keyword "{keyword}" for language "{lang}"')
def given_a_keyword(context, keyword, lang):
    """Set a keyword for a specific language."""
    context.keywords = [keyword]
    context.lang = lang


@when('adding a new keyword to the database')
def when_adding_new_keyword_to_the_database(context):
    """Add keywords to the catalog."""
    try:
        context.catalog.add_keywords(context.keywords)
        context.exception = None
        query = context.catalog.session.query(dao.Keyword)
        query = query.filter(dao.Keyword.text.in_(context.keywords))
        context.keyword = query.all()
    except Exception as e:
        context.exception = e


@then('the keyword "{keyword}" exists in the database')
def then_keyword_exists(context, keyword):
    """Test if the given keyword exists in the database."""
    assert context.keyword is not None
    assert len(context.keyword) == 1
    observed = context.keyword[0].text
    assert observed == keyword


@then('is a public keyword')
def then_keyword_is_public(context):
    """Test if keyword is to be exported."""
    assert context.keyword is not None
    assert len(context.keyword) == 1
    kw = context.keyword[0]
    assert kw.private is False
    assert kw.person is False


@then('can have synonyms exported')
def then_keyword_export_synonyms(context):
    """Test if keyword synonyms are to be exported."""
    assert context.keyword is not None
    assert context.keyword is not None
    assert len(context.keyword) == 1
    kw = context.keyword[0]
    assert kw.export_synonyms is True


@then('has {count:d} synonyms')
def then_keyword_has_no_synonyms(context, count):
    """Test if the keyword has the right number of synonyms."""
    assert context.keyword is not None
    assert context.keyword is not None
    assert len(context.keyword) == 1
    kw = context.keyword[0]
    observed = len(kw.synonyms)
    print("Synonyms:", kw.synonyms)
    print("OBSERVED:", len(kw.synonyms))
    assert observed == count
