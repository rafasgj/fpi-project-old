Feature: Ingest files into the catalog.
    As a User,
    I want to ingest files into the system catalog,
    So that the assets are managed through the system.

Scenario: Add a file at its original location.
    Given the command to ingest assets
        And the option to add a new file at its position
        And an empty catalog named "test_catalog.fpicat"
        And a device mounted at "data/samples"
        And an image file at "data/samples/DCIM/100FPIAM/FPI_0001.JPG"
    When ingesting assets into the catalog
    Then one asset is in the catalog with its attributes
        And the destination file attributes are stored within the asset
            | device_id | filename     | path           |
            |    1794   | FPI_0001.JPG | /DCIM/100FPIAM |
        And the asset id is the MD5 hash "4613ad3fd0c246dd5bb96b33b09c2996"
        And its import time is within 2 seconds from the current time
        And the import session title is the UTC time when the scenario started
        And no exception is raised

Scenario: Add several files at their original locations.
    Given the command to ingest assets
        And the option to add a new file at its position
        And an empty catalog named "test_catalog.fpicat"
        And a device mounted at "data/samples"
        And a list of files
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0001.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0002.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0003.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0004.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0005.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0006.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0007.JPG |
    When ingesting assets into the catalog
    Then there are 7 assets is the catalog, with its attributes
        And the destination file attributes are stored within the asset
        | device_id | filename     | path           |
        |    1794   | FPI_0001.JPG | /DCIM/100FPIAM |
        |    1794   | FPI_0002.JPG | /DCIM/100FPIAM |
        |    1794   | FPI_0003.JPG | /DCIM/100FPIAM |
        |    1794   | FPI_0004.JPG | /DCIM/100FPIAM |
        |    1794   | FPI_0005.JPG | /DCIM/100FPIAM |
        |    1794   | FPI_0006.JPG | /DCIM/100FPIAM |
        |    1794   | FPI_0007.JPG | /DCIM/100FPIAM |
        And the assets id is a MD5 hash
        | filename     | hash                             |
        | FPI_0001.JPG | 4613ad3fd0c246dd5bb96b33b09c2996 |
        | FPI_0002.JPG | 3b1479d722fbe11df5677bb521e2575b |
        | FPI_0003.JPG | 123b707265158269808f78573e736a6e |
        | FPI_0004.JPG | f5737b7e1d7b25662f74b885fa545b02 |
        | FPI_0005.JPG | 8dde366bfc65efd9fabcc74728061740 |
        | FPI_0006.JPG | d41d8cd98f00b204e9800998ecf8427e |
        | FPI_0007.JPG | c8b07cb389edaaf736b2486361b5e593 |
        And no exception is raised

Scenario: Add a file at its original location, for a named session.
    Given the command to ingest assets
        And the option to add a new file at its position
        And a session name of "import session"
        And an empty catalog named "test_catalog.fpicat"
        And a device mounted at "data/samples"
        And an image file at "data/samples/DCIM/100FPIAM/FPI_0001.JPG"
    When ingesting assets into the catalog
    Then one asset is in the catalog with its attributes
        And the import session title is "import session"
        And no exception is raised

Scenario: Add all files in a directory, at their original locations.
    Given the command to ingest assets
        And the option to add a new file at its position
        And an empty catalog named "test_catalog.fpicat"
        And a device mounted at "data/samples"
        And the source directory "data/samples/DCIM/100FPIAM"
    When ingesting assets into the catalog
    Then there are 7 assets is the catalog, with its attributes
        And the destination file attributes are stored within the asset
        | device_id | filename     | path           |
        |    1794   | FPI_0001.JPG | /DCIM/100FPIAM |
        |    1794   | FPI_0002.JPG | /DCIM/100FPIAM |
        |    1794   | FPI_0003.JPG | /DCIM/100FPIAM |
        |    1794   | FPI_0004.JPG | /DCIM/100FPIAM |
        |    1794   | FPI_0005.JPG | /DCIM/100FPIAM |
        |    1794   | FPI_0006.JPG | /DCIM/100FPIAM |
        |    1794   | FPI_0007.JPG | /DCIM/100FPIAM |
        And the assets id is a MD5 hash
        | filename     | hash                             |
        | FPI_0001.JPG | 4613ad3fd0c246dd5bb96b33b09c2996 |
        | FPI_0002.JPG | 3b1479d722fbe11df5677bb521e2575b |
        | FPI_0003.JPG | 123b707265158269808f78573e736a6e |
        | FPI_0004.JPG | f5737b7e1d7b25662f74b885fa545b02 |
        | FPI_0005.JPG | 8dde366bfc65efd9fabcc74728061740 |
        | FPI_0006.JPG | d41d8cd98f00b204e9800998ecf8427e |
        | FPI_0007.JPG | c8b07cb389edaaf736b2486361b5e593 |
        And no exception is raised

Scenario: Recursively add files from a directory, at their original locations.
    Given the command to ingest assets
        And the option to add a new file at its position
        And an empty catalog named "test_catalog.fpicat"
        And a device mounted at "data/samples"
        And the source directory "data/samples/DCIM"
        And the option to ingest recursively
    When ingesting assets into the catalog
    Then there are 7 assets is the catalog, with its attributes
        And the destination file attributes are stored within the asset
        | device_id | filename     | path           |
        |    1794   | FPI_0001.JPG | /DCIM/100FPIAM |
        |    1794   | FPI_0002.JPG | /DCIM/100FPIAM |
        |    1794   | FPI_0003.JPG | /DCIM/100FPIAM |
        |    1794   | FPI_0004.JPG | /DCIM/100FPIAM |
        |    1794   | FPI_0005.JPG | /DCIM/100FPIAM |
        |    1794   | FPI_0006.JPG | /DCIM/100FPIAM |
        |    1794   | FPI_0007.JPG | /DCIM/100FPIAM |
        And the assets id is a MD5 hash
        | filename     | hash                             |
        | FPI_0001.JPG | 4613ad3fd0c246dd5bb96b33b09c2996 |
        | FPI_0002.JPG | 3b1479d722fbe11df5677bb521e2575b |
        | FPI_0003.JPG | 123b707265158269808f78573e736a6e |
        | FPI_0004.JPG | f5737b7e1d7b25662f74b885fa545b02 |
        | FPI_0005.JPG | 8dde366bfc65efd9fabcc74728061740 |
        | FPI_0006.JPG | d41d8cd98f00b204e9800998ecf8427e |
        | FPI_0007.JPG | c8b07cb389edaaf736b2486361b5e593 |
        And no exception is raised
