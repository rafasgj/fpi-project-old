Feature: Manage IPTC attributes.

Scenario: Add a Caption to an image.
    Given a catalog named "test_catalog" with some assets
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0001.JPG |
    #When setting the caption of some assets.
    #| asset                            | image | caption            |
    #| 4613ad3fd0c246dd5bb96b33b09c2996 |   1   | This is a caption. |
    When setting the iptc fields of some assets
    | asset                            | image | field   | value              |
    | 4613ad3fd0c246dd5bb96b33b09c2996 |   1   | caption | This is a caption. |
    Then no exception is raised
        And the asset "4613ad3fd0c246dd5bb96b33b09c2996" iptc field caption is "This is a caption."

Scenario: Ingest images with captions.
    Given a catalog named "test_catalog" with some assets
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0001.JPG |
    Then no exception is raised
        And the asset "4613ad3fd0c246dd5bb96b33b09c2996" iptc field caption is "Resolution test chart for use with ISO Standard 12233"

Scenario: Ingest images with title.
    Given a catalog named "test_catalog" with some assets
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0003.JPG |
    Then no exception is raised
        And the asset "123b707265158269808f78573e736a6e" iptc field title is "The title"

Scenario: Add a Title to an image.
    Given a catalog named "test_catalog" with some assets
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0003.JPG |
    When setting the iptc fields of some assets
    | asset                            | image | field | value         |
    | 123b707265158269808f78573e736a6e |   1   | title | Another title |
    Then no exception is raised
        And the asset "123b707265158269808f78573e736a6e" iptc field title is "Another title"
