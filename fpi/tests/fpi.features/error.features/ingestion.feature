Feature: Warn users of ingestion errors.

@copy
Scenario Outline: Add a file twice to the catalog, and it should not be allowed.
    Given the command to ingest assets
        And the ingestion method <method>
        And the target directory "data/catalog/pics"
        And an empty catalog named "test_catalog"
        And a device mounted at "data/samples"
        And a list of files
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0001.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0001.JPG |
    When ingesting assets into the catalog
    Then an "Exception" is raised saying "Ingesting an asset already in the catalog."
        And one asset is in the catalog with its attributes
        And the asset id is the MD5 hash "4613ad3fd0c246dd5bb96b33b09c2996"

    Examples:
    | method |
    | add    |
    | copy   |

@copy @move
Scenario Outline: Fail to copy or move files to an invalid target directory.
    Given the command to ingest assets
        And the ingestion method <method>
        And the target directory "data/originals/FPI_0001.JPG"
        And an empty catalog named "test_catalog"
        And an image file at "data/originals/FPI_0001.JPG"
    When ingesting assets into the catalog
    Then an "Exception" is raised saying "Cannot use target directory."

    Examples:
    | method |
    | move   |
    | copy   |

@copy @move
Scenario Outline: No file is given to ingest.
    Given the command to ingest assets
        And the ingestion method <method>
        And the target directory "test_catalog/pictures"
        And an empty catalog named "test_catalog"
    When ingesting assets into the catalog
    Then an "Exception" is raised saying "No item to ingest."
        And the directory "test_catalog/pictures" does not exist

    Examples:
    | method |
    | move   |
    | copy   |
