Feature: Manage asset flags (pick/reject/none) and use them to search assets.
    As a user,
    I want to add flags to my assests,
    So that I can easily select or exclude assets flagged.

Scenario Outline: Add flags to images.
    Given a catalog named "test_catalog.fpicat" with some assets
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0001.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0002.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0003.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0004.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0005.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0006.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0007.JPG |
    When setting the flag of <image> of <asset> to <flag>
    Then no exception is raised
        And the flag of <image> of <asset> to <flag> is set

    Examples:
    | asset                            | image | flag      |
    | 3b1479d722fbe11df5677bb521e2575b |   1   | pick      |
    | 3b1479d722fbe11df5677bb521e2575b |   1   | reject    |
    | c8b07cb389edaaf736b2486361b5e593 |   1   | pick      |
    | c8b07cb389edaaf736b2486361b5e593 |   1   | reject    |
    | 8dde366bfc65efd9fabcc74728061740 |   1   | unflagged |
