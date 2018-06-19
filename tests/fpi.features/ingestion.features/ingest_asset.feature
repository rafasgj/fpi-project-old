Feature: Ingest files into the catalog.
    As a User,
    I want to ingest files into the system catalog,
    So that the assets can be managed by the system.

@copy @move
Scenario Outline: Ingest files in the catalog using only the catalog name.
    Given the command to ingest assets
        And the ingestion method <method>
        And an empty catalog named "test_catalog"
        And a device mounted at "data/samples"
        And the source directory "data/originals"
        And the target directory "data/catalog/pics"
        And the option to ingest recursively
    When ingesting assets into the catalog
    Then no exception is raised
        And there are 7 assets is the catalog, with its attributes
        And the assets id is a MD5 hash
        | filename     | hash                             |
        | FPI_0001.JPG | 4613ad3fd0c246dd5bb96b33b09c2996 |
        | FPI_0002.JPG | 3b1479d722fbe11df5677bb521e2575b |
        | FPI_0003.JPG | 123b707265158269808f78573e736a6e |
        | FPI_0004.JPG | f5737b7e1d7b25662f74b885fa545b02 |
        | FPI_0005.JPG | 8dde366bfc65efd9fabcc74728061740 |
        | FPI_0006.JPG | 5776c5ce1acce6475244b0d21092689e |
        | FPI_0007.JPG | c8b07cb389edaaf736b2486361b5e593 |

    Examples:
    | method |
    | move   |
    | copy   |
    | add    |

Scenario: Ingest a file that do not have a thumbnail.
Given the command to ingest assets
    And the ingestion method add
    And an empty catalog named "test_catalog"
    And an image without an embedded thumbnail "data/samples/DCIM/100FPIAM/FPI_0006.JPG"
When ingesting assets into the catalog
Then no exception is raised
    And the assets id is a MD5 hash
    | filename     | hash                             |
    | FPI_0006.JPG | 5776c5ce1acce6475244b0d21092689e |
