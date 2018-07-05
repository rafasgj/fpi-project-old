# f/π Roadmap

## Version α-1

### Catalog

fpi catalog --new catalog_name

> Creates a new empty catalog.

### Ingestion

fpi ingest catalog_path [options] (file_list | directory)<br/>
fpi ingest catalog_path [options] --add (file_list | directory)

> Add files from the file list or the given directory into the system.
  The files are kept in their original location.

fpi ingest catalog_path [options] --copy target_dir (file_list|directory)

> Add files from the file list or the given directory into the system.
  The files are copyed into the given target location.

fpi ingest catalog_path [options] --move target_dir (file_list|directory)

> Add files from the file list or the given directory into the system.
  The files are moved to the given target location.

### Ingestion options

--rename-rule

> This rule uses photo metadata to rename the files, using any of the
  filename generation rules. Only valid with --copy or --move.

--directory-rule

> This rule uses photo metadata to create a directory structure inside
  _target\_dir_ to store the files ingested. The directory structure is
  created using the filename generation rules. Only valid with --copy or
  --move.

--session

> Set the session name for the ingest session.

--recurse

> Search subdirectories for files. Only valid if a directory in being
  ingested.

### List files

fpi list catalog_path

> List all the files ingested into the system, and their asset id.

### List sessions

fpi session catalog_path <br/>
fpi session catalog_path --list

> List all the sessions stored in the system. Every ingestion is a
  session, and sessions can be named. (See ingestion option --session.)

### Retrieve information

fpi info catalog_path (--file | --asset | --session) _id_

> List all information available for the file or asset, or list all the
  files/assets ingested in the given session.

### Filename Generation rules.

|    Code    | Description.                                          |
| :--------- | :---------------------------------------------------- |
| %Y         | Four digit year.                                      |
| %y         | Two digit year.                                       |
| %m         | Two digit month.                                      |
| %d         | Two digit day.                                        |
| %M         | Three letter month abreviation.                       |
| %s         | Session name (set with --session)                     |
| %[N[.X]]c  | A number sequence, with N (or 1) digits starting at X |

## Version α-2

### Database

This version (and most future ones) will involve changes in the
application database, so there must be a migration tool/command that
will update the database when needed (i.e. opening an old database).

fpi catalog --upgrade

> Upgrades a catalog to the current revision.

### Set asset atttributes

fpi label catalog_path <br/>
fpi label catalog_path --list

> List all available labels.

fpi label catalog_path --add label_name

> Add a new label to the system.

fpi label catalog_path --remove label_name

> Remove a label from the system and from all the assets that were
  marked with this label.

fpi label catalog_path --set label_name asset_id ...

> Apply the label to all given assets.

fpi attrib catalog_path --attribute=value ... asset_id ...

> Set the value of one or more attributes of a list of asset assets
  ingested into the system.

|  Attribute  | Valid values                                        |
| :---------: | :-------------------------------------------------- |
|  --rating   | Numerical: 0-5.                                     |
|  --flag     | String: One of pick (p), unpick (u) or rejected (x) |

fpi list catalog_path criteria

> Search for assets that matches the given criteria.

  | Attribute Type |    Operators                   |
  | :------------- | :----------------------------: |
  | Numerical      | =, <, <=, >, >=                |
  | String         | =, <>                          |
  | Date           | =, <, before, <=, >, after, >= |

> Multiple expressions may be associated with operators 'and',
  meaning logical AND, and operator 'or', meaning logical 'or'.

> For this version, the attributes that can be searched for are:
   * Rating (Numerical)
   * Label (String)
   * Flag (String)
   * Filename (String)
   * Session (String)
   * Ingestion (Date)
   * Exif:CreateDate (Date)

## Version α-3

This version will expand the metadata handled by the 'search' and 'info'
commands by including EXIF, IPTC and XMP fields extracted from the
assets.

The attributes option is expanded with the following attributes:

|  Attribute     | Valid values   |
| :------------- | :------------- |
| --caption      | Text.          |
| --title        | Text.          |
| --creator      | Text.          |
| --identity _field_ | Text.      |
| --city         | Text.          |
| --country      | Text.          |
| --sublocation  | Text.          |
| --copyright    | Text.          |
| --creditline   | Text.          |
| --instructions | Text.          |
| --usage        | Text.          |
| --copyrighturl | Text.          |
| --event        | Text.          |
| --jobtitle     | Text.          |
| --headline     | Text.          |

The available identity fields are:
- address
- city
- region
- country
- zipcode
- phone
- email.

### keywords

This version allows attributing hierarchycal keywords to an asset. Each keyword
may have some properties:
- Person Keywords (implies Private Keyword)
- Private Keyword
- Export parent keywords
- Export Synonyms

Each keyword have a list of synonyms.

Searching for keywords do not ignore private or person keywords, and also is
performed on synonyms.

fpi attrib catalog_path --keyword --create _keyword:hier_ [options]

> Create a new keyword, with the given options.

| Option | Meaning |
| :-------- | :----------------------------- |
| --person  | creates a keyword that identifies someone. This implies --private. |
| --private | creates a keyword that will not be exported. |
| --synonyms [s1 s2 s3 ...] | provides synonyms for the keyword. |
| --export-synonyms | allow export of synonyms |
| --public | removes the 'private' attribute. Invalid for person keywords. |
| --no-person | removes the 'person' attribute, but not the 'private'. |
| --no-synonyms | do not export synonyms. |
| --lang *language_code* | the keyword language code. |

fpi attrib catalog_path --keyword --list

> List all available keywords.

fpi attrib catalog_path --keyword --search _criteria_

> search all keywords matching _criteria_ and its hierarchy.

fpi attrib catalog_path --keyword --remove _keyword_ [--force]

> Removes a single keyword from the database if it has no children. **--force**
will force removal, even if any asset has the keyword.

## Version α-4

### IPTC Metadata

This version will add support for changing the creator and copyright
metadata, via IPTC tags.

Both 'info' and 'search' commands might be affected by this change.

### Presets

fpi preset catalog_path --add preset_type preset_name preset_file


> Type: ingest<br/>
  Add a new ingestion preset to the system. The preset file can have
  any of the following:

  | Option     | Type    | Description                                 |
  | :--------- | :------ | :------------------------------------------ |
  | renameRule | String  | The rename rule to use.                     |
  | dirRule    | String  | The directory creation rule to use.         |
  | recurse    | Boolean | If recursive search of files is to be used. |
  | metadata   | String  | File name for the IPTC metadata preset.     |
  | session    | String  | The session name.                           |
  | targetDir  | String  | The target directory, or ?ASK.              |

> Type: metadata<br/>
  Add a new metadata preset to the system. The preset file will have a
  number of IPTC tags that will be defined later.

### Ingestion Options

This version will add the following ingestion options:

* --metadata metadata_preset

> Set the ingested assets creator and copyright to the metadata
  preset.

* --metadata field:value

> Upon ingestion, for each ingested asset, set the metadata field to the
given value

* --preset preset_name

> Perform ingestion with the given ingestion preset.

## Version β-1

This version will add a GTK+ GUI that can display previews of the assets
ingested in the system, along with queries to filter the images displayed,
and an UI to filter assets based on Rating (stars), Labels and Flags.

### Set attribute value

fpi label catalog_path --add label name \[color name\]

> Add a new label to the system and optionally attribute a color to it.
  The available colors are:

>* red
>* green
>* yellow
>* blue
>* magenta
>* orange
>* cyan
>* white
