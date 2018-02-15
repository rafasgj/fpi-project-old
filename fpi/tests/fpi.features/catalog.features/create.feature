Feature: Create a new f/π catalog.
    As a User,
    I want to create a new f/π catalog,
    So that it will be used by the system to store its data.

Scenario: Create a new f/π catalog.
    Given the command to manage a catalog
        And the option to create a new catalog
        And a catalog named "test_catalog"
    When creating a new catalog
    Then a directory with the catalog name exists with the catalog file inside
        And an empty catalog is created with the given name
        And no exception is raised

Scenario: Refuse to create f/π catalog because it exists.
Given the command to manage a catalog
        And the option to create a new catalog
        And a catalog named "test_catalog"
        And that a catalog with the same name exists
    When creating a new catalog
    Then an "Exception" is raised saing "Refusing to overwrite catalog."
