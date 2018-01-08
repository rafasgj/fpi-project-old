Feature: Create a new f/π catalog.
    As a User,
    I want to create a new f/π catalog,
    So that it will be used by the system to store its data.

Scenario: Create a new f/π catalog.
    Given the option to create a new catalog
        And a valid catalog name as "test_catalog"
    When creating a new catalog
    Then an empty catalog is created with the given name.
