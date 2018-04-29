Feature: Create a new f/π catalog.
    As a User,
    I want to create a new f/π catalog,
    So that it will be used by the system to store its data.

Scenario Outline: Create a new f/π catalog.
    Given the command to manage a catalog
        And the option to create a new catalog
        And a catalog named "<catalog_name>"
    When creating a new catalog
    Then a directory with the catalog name exists with the catalog file inside
        And an empty catalog is created with the given name
        And no exception is raised

    Examples:
    | catalog_name        |
    | test_catalog        |
    | test_catalog.fpicat |

Scenario Outline: Refuse to create f/π catalog because it exists.
Given the command to manage a catalog
        And the option to create a new catalog
        And a catalog named "<catalog_name>"
        And that a catalog with the same name exists
    When creating a new catalog
    Then an "Exception" is raised saying "Refusing to overwrite catalog"

    Examples:
    | catalog_name        |
    | test_catalog        |
    | test_catalog.fpicat |
