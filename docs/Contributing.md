# Contributing to f/π

There are many ways to contriubte to [f/π]:

* [using and evaluating](#usage)
* [contributing feature requests](#features)
* [contributing bug reports](#bugs)
* [contributing documentation](#docs)
* [contributing with code](#code)

As with any open source project, [f/π] will evolve better and faste if
people collaborate in its development. And there is no such thing as an
invaluable contribution, any help you can provide is of great value.

## Setting Up A Development Environment

To contribute to f/π's development, you'll need:

* Python 3.5 (or later)
* Git-lfs

Python 3.5 is supported by all major Linux distributions. Under macOS
follow the instructions on [Python.org](https://python.org).

[Git-lfs](https://git-lfs.github.com) makes the support for large binary
files under Git much more efficient, and is easily installed on any
current Linux distro. Under macOS, it is available through
[Homebrew](https://brew.sh).

As the project uses some Python modules that are not usually found on
standard Python setups, so you will need to install the modules:

* behave
* flake8
* flake8-docstrings
* pygobject
* alembic
* sqlalchemy
* sqlalchemy-utils

Also, some commom modules are used:

* Pillow

It is suggested that you install all of them through _pip_:

```bash
python3 -m pip install --user -r requirements.txt
```

Or install each package, one by one. If installing the packages
individually, make sure you use the correct versions

You will also need a source code editor, and you can use any editor you
prefer.

## Source Editors

### Atom

If using [Atom], it is suggested that you use version 1.19 or later, and
install the packages (shown with dependencies):

* language-gherkin:1.0.4
* linter:2.2.0
* linter-flake8:2.3.0
  * linter-ui-default:1.6.10
    * intentions:1.1.5
    * busy-signal:1.4.3

### Microsoft's Visual Studio Code

If using Microsoft's [Visual Studio Code], it is suggested that you use
the latest version, and install the extensions:

* Python
* Cucumber (Gherkin) Full Suport
* markdownlint
* Markdown Preview Github Styling
* Github

## Reporting a bug

Although f/π is well tested, you might encounter yourself in a situation
that do not work as expected. In such case, you can contribute by
reporting the situation that happened. To report a bug, create an issue
in the project's Github repository.

Before reporting a bug, search for the open issues to see if it has not
yet been reported. If the bug has not been reported, create a new issue,
if it has been reported, you can add your specific case as a comment to
the existing issue.

## Requesting a New Feature <span id="features"/>

When requesting a new feature in f/π, please fill out a new issue.
Please provide example use cases. Describe what you want to do, how you
want to do, and why you want to do what the new feature will provide.

Before you issue a new feature request, please search the open issues to
see if the feature you are requesting wasn't already requested. If the
feature exists as an open issue, simply add a comment to the issue,
with your sepecific use case.

The more you explain about why you need a feature, the more likely that
your needs are understood by developers, and better (and faster) your
fearture request is implemented.

If possible, use the following template to write your feature request
(the **And** parts are not required):

```gherkin
Given that <>,
    And <> ...
When <>,
    And <> ...
Then <>,
    And <> ...
```

## Contributing Code <span id="code"/>

f/π development happens on Github. Code contributions should be
submitted there, through merge requests.

Your merge requests should:

* Provide a test scenario that describe what you are trying to
accomplish, and which inputs you will use;
* Fix one issue and fix it well;
* Fix the issue, but do not include extraneous refactoring or code
reformatting. Refactoring should be an issue on itself;
* Have descriptive titles and descriptions;

Have commits that follow these rules:

* Do not commit any code if it does not comply with [PEP8]. Run [Flake8]
on the code to ensure it;
* Create a description of one line with, at most, 72 characters long;
* If needed you can add more lines, with no more than 72 characters
each;
* The final line of the body references the issue appropriately. If the
commit fixes the issue, add "Fixes #\<issue\>";
* It is suggested that you use the .gitcommittemplate file, as a commit
template.

----
[atom]:https://atom.io
[f/π]:http://rafaeljeffman.com?fpi
[flake8]:https://gitlab.com/pycqa/flake8
[PEP8]:https://www.python.org/dev/peps/pep-0008/
