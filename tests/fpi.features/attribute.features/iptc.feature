Feature: Manage IPTC attributes.

Scenario Outline: Ingest images with IPTC fields.
    Given a catalog named "test_catalog" with some assets
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0003.JPG |
    When setting the iptc <field> of asset <asset_id>/<img> with value <value>
    Then no exception is raised
        And the asset "<asset_id>" iptc field <field> is "<value>"
    Examples:
    | asset_id                         | img | field    | value               |
    | 123b707265158269808f78573e736a6e |  1  | jobtitle | Creator's Job Title |
    | 123b707265158269808f78573e736a6e |  1  | creator  | Creator             |
    | 123b707265158269808f78573e736a6e |  1  | title    | Another title       |
    | 123b707265158269808f78573e736a6e |  1  | caption  | The description aka caption |
    | 123b707265158269808f78573e736a6e |  1  | city     | City (legacy) |

Scenario Outline: Set various IPTC fields in an image.
    Given a catalog named "test_catalog" with some assets
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0003.JPG |
    When setting the iptc <field> of asset <asset_id>/<img> with value <value>
    Then no exception is raised
        And the asset "<asset_id>" iptc field <field> is "<value>"
    Examples:
    | asset_id                         | img | field    | value              |
    | 123b707265158269808f78573e736a6e |  1  | jobtitle | An Artist          |
    | 123b707265158269808f78573e736a6e |  1  | creator  | Artist             |
    | 123b707265158269808f78573e736a6e |  1  | title    | The title          |
    | 123b707265158269808f78573e736a6e |  1  | caption  | This is a caption. |
    | 123b707265158269808f78573e736a6e |  1  | city     | Hometown |
