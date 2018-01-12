Feature: Ingest files at their original location.
    As a User,
    I want to ingest files into the system at their current location,
    So that the assets are managed through the system.

Scenario: Add a file at their original location.
    Given the path to an image file in its final location
        And the path to a f/π catalog
    When ingesting assets into the catalog and keep its location
    Then the file metadata is found in the catalog.
