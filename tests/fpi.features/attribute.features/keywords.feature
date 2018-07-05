Feature: Manage Keywords database.
    As a user,
    I want to manage the keywords database,
    So that I can apply keywords to the image easily.

Scenario: Add a keyword to the database.
    Given a catalog named "test_catalog.fpicat" with some assets
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0001.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0002.JPG |
        And the keyword "A Keyword" for language "en-US"
    When adding a new keyword to the database
    Then no exception is raised
        And the keyword "A Keyword" exists in the database
        And is a public keyword
        And can have synonyms exported
        And has 0 synonyms

Scenario: Add multiple keywords to the database.

Scenario: Add a keyword hierarchy to the database.

Scenario: Add a keyword to an existing hierarchy.

Scenario: Apply a keyword that do not exist in the database to an asset.

Scenario: Apply a keyword that does exist in the database to an asset.

Scenario: Apply a keyword hierarchy that does exist in the database to an asset.

Scenario: Apply a keyword that does exist, but is in a hierarchy to an asset.

Scenario: Remove a keyword from the database, that was applied to assets.
# Should fail

Scenario: Force removal of a keyword from the database, that was applied to assets.
# Should warn, only on the interface.

Scenario: Remove a leaf keyword from the database.

Scenario: Remove a non-leaf keyword from the database.
# Should fail

Scenario: Modify properties of a keyword.

Scenario: Modify a keyword.

Scenario: Add a keyword that already exists in the database.

Scenario: Ingest an asset with keywords.

Scenario: Ingest an asset with hierarchical keywords.

Scenario: Ingest an asset with Adobe Lightroom hierarchycal keywords.

Scenario: Add a keyword with synonyms to the database.

Scenario: Add synonyms to a keyword in the database.

Scenario: Search for a keyword.

Scenario: Search for a keyword using a synonym.
