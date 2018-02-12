@copy
Feature: Ingest files into the catalog, by copying them.
    As a User,
    I want to ingest files in the catalog by copying them,
    So that the files are not stored in memory cards, and I have
        multiple copies of them.

Scenario: Add a file to the catalog by copying it to another location.
    Given the command to ingest assets
        And the option to ingest by copy
        And the target directory "data/catalog/pics"
        And an empty catalog file named "test_catalog.fpicat"
        And a device mounted at "data/samples"
        And an image file at "data/samples/DCIM/100FPIAM/FPI_0001.JPG"
    When ingesting assets into the catalog
    Then no exception is raised
        And one asset is in the catalog with its attributes
        And the asset id is the MD5 hash "4613ad3fd0c246dd5bb96b33b09c2996"
        And its import time is within 2 seconds from the current time
        And the import session title is the UTC time when the scenario started
        And the original files are in their original places
        And the destination files are in their respective places
        | filename                       |
        | data/catalog/pics/FPI_0001.JPG |

Scenario: Add several files by copying them to another location.
    Given the command to ingest assets
        And the option to ingest by copy
        And the target directory "data/catalog/pics"
        And an empty catalog file named "test_catalog.fpicat"
        And a device mounted at "data/samples"
        And a list of files
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0001.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0002.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0003.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0004.JPG |
    When ingesting assets into the catalog
    Then no exception is raised
        And there are 4 assets is the catalog, with its attributes
        And the assets id is a MD5 hash
        | filename     | hash                             |
        | FPI_0001.JPG | 4613ad3fd0c246dd5bb96b33b09c2996 |
        | FPI_0002.JPG | 3b1479d722fbe11df5677bb521e2575b |
        | FPI_0003.JPG | 123b707265158269808f78573e736a6e |
        | FPI_0004.JPG | f5737b7e1d7b25662f74b885fa545b02 |
        And the original files are in their original places
        And the destination files are in their respective places
        | filename                       |
        | data/catalog/pics/FPI_0001.JPG |
        | data/catalog/pics/FPI_0002.JPG |
        | data/catalog/pics/FPI_0003.JPG |
        | data/catalog/pics/FPI_0004.JPG |
