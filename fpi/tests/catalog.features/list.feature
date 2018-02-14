Feature: List assets in a catalog.
    As a User,
    I want the list the assets stored in a catalog.
    So that I can view information about the asset.

Scenario: List assets in the catalog.
    Given the command to list assets in the catalog
        And an empty catalog named "test_catalog.fpicat"
        And the catalog has some assets
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0001.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0002.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0003.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0004.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0005.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0006.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0007.JPG |
    When listing all assets in the catalog
    Then I expect all the assets to be listed, with their id and full path
| fullpath                                | id                               |
| data/samples/DCIM/100FPIAM/FPI_0001.JPG | 4613ad3fd0c246dd5bb96b33b09c2996 |
| data/samples/DCIM/100FPIAM/FPI_0002.JPG | 3b1479d722fbe11df5677bb521e2575b |
| data/samples/DCIM/100FPIAM/FPI_0003.JPG | 123b707265158269808f78573e736a6e |
| data/samples/DCIM/100FPIAM/FPI_0004.JPG | f5737b7e1d7b25662f74b885fa545b02 |
| data/samples/DCIM/100FPIAM/FPI_0005.JPG | 8dde366bfc65efd9fabcc74728061740 |
| data/samples/DCIM/100FPIAM/FPI_0006.JPG | d41d8cd98f00b204e9800998ecf8427e |
| data/samples/DCIM/100FPIAM/FPI_0007.JPG | c8b07cb389edaaf736b2486361b5e593 |
        And no exception is raised

Scenario: List sessions in the catalog.
    Given the command to list assets in the catalog
        And an empty catalog named "test_catalog.fpicat"
        And the catalog has some assets ingested in a session "First Session"
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0001.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0002.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0003.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0004.JPG |
        And the catalog has some assets ingested in a session "Second Session"
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0005.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0006.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0007.JPG |
    When listing all sessions in the catalog
    Then I expect all the session names to be listed
        | session        |
        | First Session  |
        | Second Session |
        And I expect the session names to be unique
        And no exception is raised
