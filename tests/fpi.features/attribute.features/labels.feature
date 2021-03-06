Feature: Manage asset labels and use them to search assets.
    As a user,
    I want to add labels to my assests,
    So that I can search for assets that share a common label.

Scenario: Add labels to images.
    Given a catalog named "test_catalog.fpicat" with some assets
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0001.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0002.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0003.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0004.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0005.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0006.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0007.JPG |
    When setting labels to some assets
    | asset                            | image | label   |
    | 3b1479d722fbe11df5677bb521e2575b |   1   | label_a |
    | 123b707265158269808f78573e736a6e |   1   | label_b |
    | c8b07cb389edaaf736b2486361b5e593 |   1   | label_b |
    | 5776c5ce1acce6475244b0d21092689e |   1   | label_a |
    | 8dde366bfc65efd9fabcc74728061740 |   1   | label_a |
    Then no exception is raised
        And the asset "3b1479d722fbe11df5677bb521e2575b" has the label "label_a"
        And the asset "c8b07cb389edaaf736b2486361b5e593" has the label "label_b"
        And the asset "4613ad3fd0c246dd5bb96b33b09c2996" has no label.
#        And there are 3 assets with the label "label_a"
#        And there are 2 assets with no label
        
