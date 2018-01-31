Feature: Ingest files into the catalog.
    As a User,
    I want to ingest files into the system catalog,
    So that the assets are managed through the system.

Scenario: Add a file at its original location.
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

Scenario: Add several files at their original location.
    Given the command to ingest assets
        And the option to add a new file at its position
        And an empty catalog file named "test_catalog.fpicat"
        And a device mounted at "data/samples"
        And a list of files
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0001.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0002.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0003.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0004.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0005.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0006.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0007.JPG |
    When ingesting assets into the catalog
    Then there are 7 assets is the catalog, with its attributes
        And the original file attributes are stored within the asset
        | device_id | inode | filename     | path           | size    |
        |    1794   |  134  | FPI_0001.JPG | /DCIM/100FPIAM | 4342771 |
        |    1794   |  141  | FPI_0002.JPG | /DCIM/100FPIAM | 2304239 |
        |    1794   |  142  | FPI_0003.JPG | /DCIM/100FPIAM |   99942 |
        |    1794   |  143  | FPI_0004.JPG | /DCIM/100FPIAM |  207765 |
        |    1794   |  145  | FPI_0005.JPG | /DCIM/100FPIAM |  208946 |
        |    1794   |  144  | FPI_0006.JPG | /DCIM/100FPIAM |  193361 |
        |    1794   |  146  | FPI_0007.JPG | /DCIM/100FPIAM |  329856 |
        And the destination file attributes are stored within the asset
        | device_id | filename     | path           |
        |    1794   | FPI_0001.JPG | /DCIM/100FPIAM |
        |    1794   | FPI_0002.JPG | /DCIM/100FPIAM |
        |    1794   | FPI_0003.JPG | /DCIM/100FPIAM |
        |    1794   | FPI_0004.JPG | /DCIM/100FPIAM |
        |    1794   | FPI_0005.JPG | /DCIM/100FPIAM |
        |    1794   | FPI_0006.JPG | /DCIM/100FPIAM |
        |    1794   | FPI_0007.JPG | /DCIM/100FPIAM |
        And the assets id is a MD5 hash
        | filename     | hash                             |
        | FPI_0001.JPG | 58769b7023d0441be97612b5b7e69488 |
        | FPI_0002.JPG | 41f9ee23c5751da137b316b7ae2d3e1b |
        | FPI_0003.JPG | 38db4ef337ba9d08715c6536e73dfbcc |
        | FPI_0004.JPG | 4b86850cea9b4496e6a9dc55e2b692f4 |
        | FPI_0005.JPG | 5ab39d77ed78271dff0e63a4a187bbf5 |
        | FPI_0006.JPG | 0395dab50a87b5644d4f4e39f91bf73c |
        | FPI_0007.JPG | acd678725ac83a9b74bd06f58fb17f7f |
