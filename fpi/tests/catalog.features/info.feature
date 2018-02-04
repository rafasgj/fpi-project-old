Feature: Retrieve information abount an item of the catalog.
    As a User,
    I want to obtain information about itens in the catalog,
    So that I can search for the item that I want.

Scenario: Get information about a session.
    Given the command to obtain information about itens in the catalog
        And the option to obtain information abount a Session
        And the name of a session as "First Session"
        And a catalog file named as "test_catalog.fpicat"
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
    When requesting information about an item in the catalog
    Then I expect to see the session name
        And I expect to see the fullpath of the files and the asset id
        | fullpath                   | id                               |
        | /DCIM/100FPIAM/FPI_0001.JPG | 4613ad3fd0c246dd5bb96b33b09c2996 |
        | /DCIM/100FPIAM/FPI_0002.JPG | 3b1479d722fbe11df5677bb521e2575b |
        | /DCIM/100FPIAM/FPI_0003.JPG | 123b707265158269808f78573e736a6e |
        | /DCIM/100FPIAM/FPI_0004.JPG | f5737b7e1d7b25662f74b885fa545b02 |

Scenario: Get information about an asset, using the asset id.
    Given the command to obtain information about itens in the catalog
        And the option to obtain information abount as Asset
        And a catalog file named as "test_catalog.fpicat"
        And the asset id "123b707265158269808f78573e736a6e"
        And the catalog has some assets
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0001.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0002.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0003.JPG |
    When requesting information about an item in the catalog
    Then I expect to see the asset fullpath and id
        | fullpath                    | id                               |
        | /DCIM/100FPIAM/FPI_0003.JPG | 123b707265158269808f78573e736a6e |
        And the asset image information for Width, Height and Capture Date/Time
        | Width | Height |  Capture Date Time  |
        |  1000 |    500 | 2011-10-28 12:00:00 |
