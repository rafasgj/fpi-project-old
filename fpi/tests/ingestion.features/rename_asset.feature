@copy
Feature: Rename files and create directories based on its metadata and rules.
    As a User,
    I want the system to automatically rename files ro create directories
        based on asset metadata and a creation rule,
    So that the files are stored in a controlled structure.

Scenario: Rename a file using the image metadata, while copying files.
    Given the command to ingest assets
        And the option to ingest by copy
        And the target directory "data/catalog/pics"
        And an empty catalog file named "test_catalog.fpicat"
        And a device mounted at "data/samples"
        And an image file at "data/samples/DCIM/100FPIAM/FPI_0001.JPG"
        And a session name of "firstsession"
        And the rename rule "{year}-{month}-{day}_{session}"
    When ingesting assets into the catalog
    Then no exception is raised
        And the original files are in their original places
        And the destination files are in their respective places
        | filename                                      |
        | data/catalog/pics/2006-08-31_firstsession.JPG |

Scenario: Rename files using the image metadata, while copying files.
    Given the command to ingest assets
        And the option to ingest by copy
        And the target directory "data/catalog/pics"
        And an empty catalog file named "test_catalog.fpicat"
        And a device mounted at "data/samples"
        And a list of files
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0001.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0002.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0003.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0007.JPG |
        And a session name of "firstsession"
        And the rename rule "{year}-{month}-{day}_{session}"
    When ingesting assets into the catalog
    Then no exception is raised
        And the original files are in their original places
        And the destination files are in their respective places
        | filename                                      |
        | data/catalog/pics/2006-08-31_firstsession.JPG |
        | data/catalog/pics/2010-12-27_firstsession.JPG |
        | data/catalog/pics/2011-10-28_firstsession.JPG |
        | data/catalog/pics/2011-04-03_firstsession.JPG |

Scenario: Create directories using image metadata, while copying files.
    Given the command to ingest assets
        And the option to ingest by copy
        And the target directory "data/catalog/pics"
        And an empty catalog file named "test_catalog.fpicat"
        And a device mounted at "data/samples"
        And a list of files
        | filename                                |
        | data/samples/DCIM/100FPIAM/FPI_0001.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0002.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0003.JPG |
        | data/samples/DCIM/100FPIAM/FPI_0007.JPG |
        And a session name of "firstsession"
        And the rename rule "{year}-{month}-{day}_{session}"
        And the directory rule "{year}/{month}-{day}"
    When ingesting assets into the catalog
    Then no exception is raised
        And the original files are in their original places
        And the destination files are in their respective places
        | filename                                                 |
        | data/catalog/pics/2006/08-31/2006-08-31_firstsession.JPG |
        | data/catalog/pics/2010/12-27/2010-12-27_firstsession.JPG |
        | data/catalog/pics/2011/10-28/2011-10-28_firstsession.JPG |
        | data/catalog/pics/2011/04-03/2011-04-03_firstsession.JPG |
