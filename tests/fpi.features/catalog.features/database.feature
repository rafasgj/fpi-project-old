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
Scenario: Try to verify the revision of a catalog that does not exist.
    When I request the version of a catalog that does not exist.
    Then an exception "errors.InexistentCatalog" is raised
