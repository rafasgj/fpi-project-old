Feature: Create a new f/π catalog.
    As a User,
    I want to create a new f/π catalog,
    So that it will be used by the system to store its data.

Scenario: Create a new f/π catalog.
    Given the option to create a new catalog
        And a catalog named "test_catalog"
    When creating a new catalog
    Then an empty catalog is created with the given name
        And there is no Asset in the catalog.

Scenario: Refuse to create f/π catalog because it exists.
    Given the option to create a new catalog
        And a catalog named "test_catalog"
        And the catalog exists
    When creating a new catalog
    Then an "Exception" is raised saing "Refusing to overwrite catalog."
