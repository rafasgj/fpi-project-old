Feature: Manage Keywords database.
    As a user,
    I want to manage the keywords database,
    So that I can apply keywords to the image easily.

Scenario: Add a keyword to the database.
    Given an empty catalog named "test_catalog.fpicat"
        And the keyword "A Keyword" for language "en-US"
    When adding new keywords to the database
    Then no exception is raised
        And the keyword "A Keyword" exists in the database
        And each keyword is a public keyword
        And each keyword can have synonyms exported
        And each keyword has 0 synonyms

Scenario: Add multiple keywords to the database.
    Given an empty catalog named "test_catalog.fpicat"
        And some keywords
    When adding new keywords to the database
    Then no exception is raised
        And the keywords exist in the database
        And each keyword is a public keyword
        And each keyword can have synonyms exported
        And each keyword has 0 synonyms

Scenario: Add a keyword hierarchy to the database.
    Given an empty catalog named "test_catalog.fpicat"
        And the keyword "level one:level two:leaf" for language "en-US"
    When adding new keywords to the database
    Then no exception is raised
        And the keyword "level one" exists in the database
        And the keyword "level two" exists in the database
        And the keyword "leaf" exists in the database
        And the keyword "level one" is parent of "level two"
        And the keyword "level two" is parent of "leaf"
        And the keyword "leaf" is not parent of "level one"
        And the keyword "leaf" is not parent of "level two"
        And the keyword "level two" is not parent of "level one"

Scenario: Add a keyword to an existing hierarchy.
    Given an empty catalog named "test_catalog.fpicat"
        And the keyword "level one:level two" exists
        And the keyword "level one:level two:leaf" for language "en-US"
    When adding new keywords to the database
    Then no exception is raised
        And the keyword "leaf" exists in the database
        And the keyword "level two" is parent of "leaf"
        And the keyword "leaf" is not parent of "level one"
        And the keyword "leaf" is not parent of "level two"

Scenario: Apply a keyword that do not exist in the database to an asset.
    Given a catalog named "test_catalog.fpicat" with some assets
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0001.JPG |
    When assigning the keyword "A Keyword" to the asset "4613ad3fd0c246dd5bb96b33b09c2996"
    Then no exception is raised
        And the keyword "A Keyword" exists in the database
        And the asset "4613ad3fd0c246dd5bb96b33b09c2996" has the keyword "A Keyword"

Scenario: Apply a keyword that does exist in the database to an asset.
    Given a catalog named "test_catalog.fpicat" with some assets
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0001.JPG |
        And the keyword "A Keyword" exists in the database
    When assigning the keyword "A Keyword" to the asset "4613ad3fd0c246dd5bb96b33b09c2996"
    Then no exception is raised
        And the asset "4613ad3fd0c246dd5bb96b33b09c2996" has the keyword "A Keyword"

Scenario: Apply a keyword hierarchy that does exist in the database to an asset.
    Given a catalog named "test_catalog.fpicat" with some assets
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0001.JPG |
    When assigning the keyword "level one:level two:leaf" to the asset "4613ad3fd0c246dd5bb96b33b09c2996"
    Then no exception is raised
        And the asset "4613ad3fd0c246dd5bb96b33b09c2996" has the keyword "leaf"
        And the keyword "level one" exists in the database
        And the keyword "level two" exists in the database
        And the keyword "leaf" exists in the database
        And the keyword "level one" is parent of "level two"
        And the keyword "level two" is parent of "leaf"
        And the keyword "leaf" is not parent of "level one"
        And the keyword "leaf" is not parent of "level two"
        And the keyword "level two" is not parent of "level one"

Scenario: Apply a keyword that does exist, but is in a hierarchy to an asset.
    Given a catalog named "test_catalog.fpicat" with some assets
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0001.JPG |
        And the keyword "level one:level two:leaf" exists in the database
    When assigning the keyword "level one:level two:leaf" to the asset "4613ad3fd0c246dd5bb96b33b09c2996"
    Then no exception is raised
        And the asset "4613ad3fd0c246dd5bb96b33b09c2996" has the keyword "leaf"

Scenario: Remove a keyword from the database.
    Given an empty catalog named "test_catalog.fpicat"
        And the keyword "A Keyword" exists in the database
    When removing the keyword "A Keyword"
    Then no exception is raised
        And the keyword "A Keyword" does not exist in the database

Scenario: Remove a leaf keyword from the database.
    Given an empty catalog named "test_catalog.fpicat"
        And the keyword "level one:level two:leaf" exists in the database
    When removing the keyword "leaf"
    Then no exception is raised
        And the keyword "leaf" does not exist in the database
        And the keyword "level two" has 0 children

Scenario: Remove a non-leaf keyword from the database.
    Given an empty catalog named "test_catalog.fpicat"
        And the keyword "level one:level two:leaf" exists in the database
    When removing the keyword "level two"
    Then an exception "errors.RemoveException" is raised
        And the keyword "level one" exists in the database
        And the keyword "level two" exists in the database
        And the keyword "leaf" exists in the database
        And the keyword "level one" is parent of "level two"
        And the keyword "level two" is parent of "leaf"
        And the keyword "leaf" is not parent of "level one"
        And the keyword "leaf" is not parent of "level two"
        And the keyword "level two" is not parent of "level one"

Scenario: Remove a keyword from the database, that was applied to assets.
# Should fail, with exception errors.RemoveException with message "Keyword is in use."
    Given a catalog named "test_catalog.fpicat" with some assets
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0001.JPG |
        And the keyword "level one:level two:leaf" exists in the database
        And the keyword "leaf" is assigned to asset "4613ad3fd0c246dd5bb96b33b09c2996"
    When removing the keyword "leaf"
    Then an exception "errors.RemoveException" is raised
        And the asset "4613ad3fd0c246dd5bb96b33b09c2996" has the keyword "leaf"
        And the keyword "leaf" exists in the database

Scenario: Force removal of a keyword from the database, that was applied to assets.
# Should warn, only on the interface.
    Given a catalog named "test_catalog.fpicat" with some assets
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0001.JPG |
        And the keyword "level one:level two:leaf" exists in the database
        And the keyword "leaf" is assigned to asset "4613ad3fd0c246dd5bb96b33b09c2996"
    When forcing removal of the keyword "leaf"
    Then no exception is raised
        And the asset "4613ad3fd0c246dd5bb96b33b09c2996" has 0 keywords
        And the keyword "leaf" does not exist in the database

Scenario: Unassign a keyword from an image.

Scenario: Modify properties of a keyword.

Scenario: Modify a keyword.

Scenario: Add a keyword that already exists in the database.
# shuld fail with errors.DuplicateKeyword

Scenario: Ingest an asset with keywords.

Scenario: Ingest an asset with hierarchical keywords.

Scenario: Ingest an asset with Adobe Lightroom hierarchycal keywords.

Scenario: Add a keyword with synonyms to the database.

Scenario: Add synonyms to a keyword that exists in the database.

Scenario: Search for a keyword.

Scenario: Search for a keyword using a synonym.

Scenario: Search for keywords that were not assigned to any asset.
