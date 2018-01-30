Feature: Ingest files into the catalog.
    As a User,
    I want to ingest files into the system catalog,
    So that the assets are managed through the system.

Scenario: Add a file at its original location, as a default option.
    Given the command to ingest assets
        And the option to add a new file at its position
        And an empty catalog file named "test_catalog.fpicat"
        And a device mounted at "data/samples"
        And an image file at "data/samples/DCIM/100FPIAM/FPI_0001.JPG"
    When ingesting assets into the catalog
    Then one asset is in the catalog with its attributes
        And the original file attributes are stored within the asset
            | device_id | inode | filename     | path           | size    |
            |    1794   |  134  | FPI_0001.JPG | /DCIM/100FPIAM | 4342771 |
        And the destination file attributes are stored within the asset
            | device_id | filename     | path           |
            |    1794   | FPI_0001.JPG | /DCIM/100FPIAM |
        And the asset id is the MD5 hash "58769b7023d0441be97612b5b7e69488"
        # The MD5 hash is obtained from the concatenation of:
        # - original device id as a 16-bit hexadecimal value. ("0000")
        # - inode as a 64-bit hexadecimal value. ("0000000000000000")
        # - original path whithout separators ("DCIM100FPIAM")
        # - original filename ("FPI_0001.JPG")
        # - original filesize as a 64-bit hexadecimal value.
