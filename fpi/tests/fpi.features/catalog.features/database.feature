Feature: Automatically manage catalog versions when upgrading the system.
    As a User,
    I want to have the catalog automatically updated
    When I upgrade the system
    So that I can use the new features.

@version
Scenario: The system correctly recognizes that the catalog needs an upgrade.
    Given an existing catalog named "data/catalogs/alpha_1"
        And the catalog revision is "81f865635e09"
    When I try to open the catalog
    Then an exception "errors.UnexpectedCatalogVersion" is raised

@version
Scenario: A catalog with an older version is updated to the current version.
    Given an existing catalog named "data/catalogs/alpha_1"
        And the catalog revision is "81f865635e09"
    When I try to updated it the current version
    Then no exception is raised
        And the catalog is ready for use in the current version

@version
Scenario: Trying to upgrade a catalog in the current version.
    Given an empty catalog named "current_version"
        And the catalog is ready for use in the current version
    When I try to updated it the current version
    Then an exception "errors.UnexpectedCatalogVersion" is raised