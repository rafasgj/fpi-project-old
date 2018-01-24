Feature: Ingest files into the catalog.
    As a User,
    I want to ingest files into the system catalog,
    So that the assets are managed through the system.

Scenario: Add a file at its original location, as a default option.
    Given the command to ingest assets
        And an image file at its destination location of "a/b/c/a.jpg"
        And a catalog file named "test_catalog.fpicat"
    When ingesting assets into the catalog and keep its location
    Then the file metadata is found in the catalog.

Scenario: Add a file at its original location.
    Given the command to ingest assets
        And the option to add a new file at its position
        And an image file at its destination location of "a/b/c/a.jpg"
        And a catalog file named "test_catalog.fpicat"
    When ingesting assets into the catalog and keep its location
    Then the file metadata is found in the catalog.
