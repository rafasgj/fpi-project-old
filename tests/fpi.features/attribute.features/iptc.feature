Feature: Manage IPTC attributes.

Scenario Outline: Ingest images with IPTC fields.
    Given a catalog named "test_catalog" with some assets
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0003.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0006.JPG |
    Then no exception is raised
        And the asset "<asset_id>" iptc field <field> is "<value>"
Examples:
| asset_id                         | img | field        | value               |
| 123b707265158269808f78573e736a6e |  1  | jobtitle     | Creator's Job Title |
| 123b707265158269808f78573e736a6e |  1  | creator      | Creator             |
| 123b707265158269808f78573e736a6e |  1  | title        | The title           |
| 123b707265158269808f78573e736a6e |  1  | caption      | The description aka caption |
| 123b707265158269808f78573e736a6e |  1  | city         | City (legacy)       |
| 123b707265158269808f78573e736a6e |  1  | country      | Country (legacy)    |
| 123b707265158269808f78573e736a6e |  1  | copyright    | © 2011, Copyright Notice |
| 123b707265158269808f78573e736a6e |  1  | creditline   | Credit Line         |
| 123b707265158269808f78573e736a6e |  1  | headline     | The headline        |
| 123b707265158269808f78573e736a6e |  1  | instructions | Instructions        |
| 123b707265158269808f78573e736a6e |  1  | usage        | Rights Usage Termns |
| 123b707265158269808f78573e736a6e |  1  | event        | The Event           |
| 5776c5ce1acce6475244b0d21092689e |  1  | copyrighturl | http://www.WebStatementOfRights.org/2017.1 |
| 123b707265158269808f78573e736a6e |  1  | sublocation  | Sublocation (legacy) |

Scenario Outline: Set various IPTC fields in an image.
    Given a catalog named "test_catalog" with some assets
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0003.JPG |
    When setting the iptc <field> of asset <asset_id>/<img> with value <value>
    Then no exception is raised
        And the asset "<asset_id>" iptc field <field> is "<value>"
Examples:
| asset_id                         | img | field        | value               |
| 123b707265158269808f78573e736a6e |  1  | jobtitle     | An Artist           |
| 123b707265158269808f78573e736a6e |  1  | creator      | Artist              |
| 123b707265158269808f78573e736a6e |  1  | title        | Another title       |
| 123b707265158269808f78573e736a6e |  1  | caption      | This is a caption.  |
| 123b707265158269808f78573e736a6e |  1  | city         | Hometown            |
| 123b707265158269808f78573e736a6e |  1  | country      | Brasil              |
| 123b707265158269808f78573e736a6e |  1  | copyright    | © 2018, f/π         |
| 123b707265158269808f78573e736a6e |  1  | creditline   | Credit, when due.   |
| 123b707265158269808f78573e736a6e |  1  | headline     | What it's all about |
| 123b707265158269808f78573e736a6e |  1  | instructions | Copy at will.       |
| 123b707265158269808f78573e736a6e |  1  | usage        | Don't use it.       |
| 123b707265158269808f78573e736a6e |  1  | event        | A party.            |
| 123b707265158269808f78573e736a6e |  1  | copyrighturl | https://example.com |
| 123b707265158269808f78573e736a6e |  1  | sublocation  | A nice place to be  |

Scenario: Ingest images with Creator Identification fields.
    Given a catalog named "test_catalog" with some assets
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0003.JPG |
    Then no exception is raised
        And the asset "123b707265158269808f78573e736a6e" has the complete IPTC CI fields
        | img | field             | value                              |
        |  1  | creator           | Creator                            |
        |  1  | creatoraddress    | Creator's CI: Address, line 1      |
        |  1  | creatorcity       | Creator's CI: City                 |
        |  1  | creatorregion     | Creator's CI: State/Province       |
        |  1  | creatorpostalcode | CREATOR'S CI: POSTCODE             |
        |  1  | creatorcountry    | Creator's CI: Country              |
        |  1  | creatortelephone  | Creator's CI: Phone # 1, Phone # 2 |
        |  1  | creatoremail      | Creator's CI: Email@1, Email@2     |

Scenario: Set Creator Identification fields.
    Given a catalog named "test_catalog" with some assets
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0003.JPG |
    When adjusting Creator's CI of asset "123b707265158269808f78573e736a6e"
    | img | field             | value             |
    |  1  | creator           | Rafael Jeffman    |
    |  1  | creatoraddress    | Av. Farrapos      |
    |  1  | creatorcity       | Porto Alegre      |
    |  1  | creatorregion     | Rio Grande do Sul |
    |  1  | creatorpostalcode | 90220-006         |
    |  1  | creatorcountry    | Brasil            |
    |  1  | creatortelephone  | +55 51 5555-1234  |
    |  1  | creatoremail      | rafasgj@gmail.com |
    Then no exception is raised
        And the asset "123b707265158269808f78573e736a6e" has the complete IPTC CI fields
        | img | field             | value             |
        |  1  | creator           | Rafael Jeffman    |
        |  1  | creatoraddress    | Av. Farrapos      |
        |  1  | creatorcity       | Porto Alegre      |
        |  1  | creatorregion     | Rio Grande do Sul |
        |  1  | creatorpostalcode | 90220-006         |
        |  1  | creatorcountry    | Brasil            |
        |  1  | creatortelephone  | +55 51 5555-1234  |
        |  1  | creatoremail      | rafasgj@gmail.com |
