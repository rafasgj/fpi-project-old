Feature: Warn user when trying to use a non-existing catalog.

Scenario Outline: Ingesting files in a non-existing catalog file.
    Given the command to ingest assets
        And the ingestion method <method>
        And the target directory "data/catalog/pics"
        And a catalog named "<name>"
        And a file <filename>
    When ingesting assets into the catalog
    Then an "Exception" is raised saing "Trying to use an inexistent catalog '<name>'."

    Examples:
    | method | name              | filename          |
    | add    | inexistent        | path/to/image.cr2 |
    | add    | inexistent.fpicat | path/to/image.cr2 |
    | copy   | inexistent        | path/to/image.cr2 |
    | copy   | inexistent.fpicat | path/to/image.cr2 |
    | move   | inexistent        | path/to/image.cr2 |
    | move   | inexistent.fpicat | path/to/image.cr2 |

Scenario Outline: Listing assets from a non-existing catalog file.
    Given the command to list assets in the catalog
        And a catalog named "<name>"
    When listing all assets in the catalog
    Then an "Exception" is raised saing "Trying to use an inexistent catalog '<name>'."

    Examples:
    | name              |
    | inexistent        |
    | inexistent.fpicat |

Scenario Outline: Requesting info from a non-existing catalog file.
    Given the command to obtain information about itens in the catalog
        And the option to obtain information about a Session
        And the session query as "First Session"
        And a catalog named "<name>"
    When requesting information about an item in the catalog
    Then an "Exception" is raised saing "Trying to use an inexistent catalog '<name>'."

    Examples:
    | name              |
    | inexistent        |
    | inexistent.fpicat |

Scenario Outline: Requesting info from a non-existing catalog file.
    Given the command to obtain information about itens in the catalog
        And the option to obtain information about an Asset
        And the session query as "First Session"
        And a catalog named "<name>"
    When requesting information about an item in the catalog
    Then an "Exception" is raised saing "Trying to use an inexistent catalog '<name>'."

    Examples:
    | name              |
    | inexistent        |
    | inexistent.fpicat |
