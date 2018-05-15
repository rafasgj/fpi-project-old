Feature: Automatically manage catalog versions when upgrading the system.
    As a User,
    I want to have the catalog automatically updated
    When I upgrade the system
    So that I can use the new features.

@version
Scenario: The system correctly recognizes that the database needs an upgrade.
    Given an existing catalog named "data/catalogs/alpha_1"
    When I try to open the catalog
    Then an "errors.UnexpectedCatalogVersion" is raised
