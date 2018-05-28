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
    Then no exception is raised
        And I expect 7 assets to be listed, with their id and full path
        | fullpath                    | id                               |
        | /DCIM/100FPIAM/FPI_0001.JPG | 4613ad3fd0c246dd5bb96b33b09c2996 |
        | /DCIM/100FPIAM/FPI_0002.JPG | 3b1479d722fbe11df5677bb521e2575b |
        | /DCIM/100FPIAM/FPI_0003.JPG | 123b707265158269808f78573e736a6e |
        | /DCIM/100FPIAM/FPI_0004.JPG | f5737b7e1d7b25662f74b885fa545b02 |
        | /DCIM/100FPIAM/FPI_0005.JPG | 8dde366bfc65efd9fabcc74728061740 |
        | /DCIM/100FPIAM/FPI_0006.JPG | 5776c5ce1acce6475244b0d21092689e |
        | /DCIM/100FPIAM/FPI_0007.JPG | c8b07cb389edaaf736b2486361b5e593 |

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
    Then no exception is raised
        And I expect all the session names to be listed
        | session        |
        | First Session  |
        | Second Session |
        And I expect the session names to be unique


Scenario: List flagged assets.
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
        And some images have the flag attribute set to "pick"
        | asset                            | image | flag   |
        | 3b1479d722fbe11df5677bb521e2575b |   1   | pick   |
        | c8b07cb389edaaf736b2486361b5e593 |   1   | pick   |
        | 8dde366bfc65efd9fabcc74728061740 |   1   | pick   |
    When listing assets with the flag attribute set to "pick"
    Then no exception is raised
        And I expect 3 assets to be listed, with their id and full path
        | fullpath                    | id                               |
        | /DCIM/100FPIAM/FPI_0002.JPG | 3b1479d722fbe11df5677bb521e2575b |
        | /DCIM/100FPIAM/FPI_0005.JPG | 8dde366bfc65efd9fabcc74728061740 |
        | /DCIM/100FPIAM/FPI_0007.JPG | c8b07cb389edaaf736b2486361b5e593 |

Scenario: List labeled assets.
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
        And some images have the label attribute set to "labeled"
        | asset                            | image |
        | 3b1479d722fbe11df5677bb521e2575b |   1   |
        | c8b07cb389edaaf736b2486361b5e593 |   1   |
        | 8dde366bfc65efd9fabcc74728061740 |   1   |
    When listing assets with field "label", matching exactly "labeled"
    Then no exception is raised
        And I expect 3 assets to be listed, with their id and full path
        | fullpath                    | id                               |
        | /DCIM/100FPIAM/FPI_0002.JPG | 3b1479d722fbe11df5677bb521e2575b |
        | /DCIM/100FPIAM/FPI_0005.JPG | 8dde366bfc65efd9fabcc74728061740 |
        | /DCIM/100FPIAM/FPI_0007.JPG | c8b07cb389edaaf736b2486361b5e593 |

Scenario: List rated assets.
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
        And some images have the rating attribute set to 3
        | asset                            | image |
        | 3b1479d722fbe11df5677bb521e2575b |   1   |
        | c8b07cb389edaaf736b2486361b5e593 |   1   |
        | 8dde366bfc65efd9fabcc74728061740 |   1   |
    When listing assets with the rating attribute is "equal to" 3
    Then no exception is raised
        And I expect 3 assets to be listed, with their id and full path
        | fullpath                    | id                               |
        | /DCIM/100FPIAM/FPI_0002.JPG | 3b1479d722fbe11df5677bb521e2575b |
        | /DCIM/100FPIAM/FPI_0005.JPG | 8dde366bfc65efd9fabcc74728061740 |
        | /DCIM/100FPIAM/FPI_0007.JPG | c8b07cb389edaaf736b2486361b5e593 |

Scenario: List assets by filename.
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
    When listing assets with field "filename", matching partially "FPI_0005"
    Then no exception is raised
        And I expect 1 assets to be listed, with their id and full path
        | fullpath                    | id                               |
        | /DCIM/100FPIAM/FPI_0005.JPG | 8dde366bfc65efd9fabcc74728061740 |

Scenario: List assets by filename, without case sensitivity.
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
    When filtering "filename", with case insensitive partial match to "fpi_0005"
    Then no exception is raised
        And I expect 1 assets to be listed, with their id and full path
        | fullpath                    | id                               |
        | /DCIM/100FPIAM/FPI_0005.JPG | 8dde366bfc65efd9fabcc74728061740 |

Scenario: List assets by session name.
    Given the command to list assets in the catalog
        And an empty catalog named "test_catalog.fpicat"
        And the catalog has some assets ingested in a session "First Session"
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0001.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0003.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0004.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0006.JPG |
        And the catalog has some assets ingested in a session "Second Session"
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0002.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0005.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0007.JPG |
    When listing assets with field "session", matching exactly "Second Session"
    Then no exception is raised
        And I expect 3 assets to be listed, with their id and full path
        | fullpath                    | id                               |
        | /DCIM/100FPIAM/FPI_0002.JPG | 3b1479d722fbe11df5677bb521e2575b |
        | /DCIM/100FPIAM/FPI_0005.JPG | 8dde366bfc65efd9fabcc74728061740 |
        | /DCIM/100FPIAM/FPI_0007.JPG | c8b07cb389edaaf736b2486361b5e593 |

Scenario: List assets by capture date.
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
    When listing assets with "capture_datetime", in the year 2011
    Then no exception is raised
        And I expect 4 assets to be listed, with their id and full path
        | fullpath                    | id                               |
        | /DCIM/100FPIAM/FPI_0003.JPG | 123b707265158269808f78573e736a6e |
        | /DCIM/100FPIAM/FPI_0004.JPG | f5737b7e1d7b25662f74b885fa545b02 |
        | /DCIM/100FPIAM/FPI_0005.JPG | 8dde366bfc65efd9fabcc74728061740 |
        | /DCIM/100FPIAM/FPI_0007.JPG | c8b07cb389edaaf736b2486361b5e593 |


Scenario: List assets by import date.
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
    When listing assets where "import_date" is today
    Then no exception is raised
        And I expect 7 assets to be listed, with their id and full path
        | fullpath                    | id                               |
        | /DCIM/100FPIAM/FPI_0001.JPG | 4613ad3fd0c246dd5bb96b33b09c2996 |
        | /DCIM/100FPIAM/FPI_0002.JPG | 3b1479d722fbe11df5677bb521e2575b |
        | /DCIM/100FPIAM/FPI_0003.JPG | 123b707265158269808f78573e736a6e |
        | /DCIM/100FPIAM/FPI_0004.JPG | f5737b7e1d7b25662f74b885fa545b02 |
        | /DCIM/100FPIAM/FPI_0005.JPG | 8dde366bfc65efd9fabcc74728061740 |
        | /DCIM/100FPIAM/FPI_0006.JPG | 5776c5ce1acce6475244b0d21092689e |
        | /DCIM/100FPIAM/FPI_0007.JPG | c8b07cb389edaaf736b2486361b5e593 |
