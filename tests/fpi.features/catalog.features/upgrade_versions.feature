Feature: Upgrade an existing catalog to the current version.
    As a User,
    I want my old catalog to be upgraded despite its version,
    So I can use the current version of f/π.

@version
Scenario: Trying to upgrade a catalog in the current version.
    Given an empty catalog named "current_version"
        And the catalog is ready for use in the current version
    When I try to update it the current version
    Then an exception "errors.UnexpectedCatalogVersion" is raised

@version
Scenario: Upgrade alpha_1 to current version.
    Given an existing catalog named "data/catalogs/alpha_1"
        And the catalog revision is "81f865635e09"
    When I try to update it the current version
    Then no exception is raised
        And the catalog is ready for use in the current version

@version
Scenario: Upgrade alpha_2 to current version.
    Given an existing catalog named "data/catalogs/alpha_2"
        And the catalog revision is "1b68ca65442c"
    When I try to update it the current version
    Then no exception is raised
        And the catalog is ready for use in the current version

# @version
# Scenario: Upgrade alpha_3 to current version.
#     Given an existing catalog named "data/catalogs/alpha_3"
#         And the catalog revision is "a845b60ac452"
#     When I try to update it the current version
#     Then no exception is raised
#         And the catalog is ready for use in the current version
