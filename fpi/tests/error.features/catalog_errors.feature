Feature: Ensure user errors are handled gently.
    As a User,
    I want the system to correct me if I use the system wrongly,
    So that I learn to use the system properly.

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

Scenario Outline: Requesting info from a non-existing catalog file.
    Given the command to list assets in the catalog
        And a catalog named "<name>"
    When listing all assets in the catalog
    Then an "Exception" is raised saing "Trying to use an inexistent catalog '<name>'."

    Examples:
    | name              |
    | inexistent        |
    | inexistent.fpicat |
