Feature: Manage IPTC attributes.

Scenario: Add a Caption to the image.
    Given a catalog named "test_catalog" with some assets
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0001.JPG |
    When setting the caption of some assets.
    | asset                            | image | caption            |
    | 4613ad3fd0c246dd5bb96b33b09c2996 |   1   | This is a caption. |
    Then no exception is raised
        And the asset "4613ad3fd0c246dd5bb96b33b09c2996" has the caption "This is a caption."

Scenario: Ingest images with captions.
    Given a catalog named "test_catalog" with some assets
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0001.JPG |
    Then no exception is raised
        And the asset "4613ad3fd0c246dd5bb96b33b09c2996" has the caption "Resolution test chart for use with ISO Standard 12233"
