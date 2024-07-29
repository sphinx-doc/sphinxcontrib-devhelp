Release 2.0.0 (2024-07-28)
==========================

* Adopt Ruff
* Tighten MyPy settings
* Update GitHub actions versions
* Avoid storing build time in gzip headers

Release 1.0.6 (2024-01-13)
==========================

* Remove Sphinx as a required dependency, as circular dependencies may cause
  failure with package managers that expect a directed acyclic graph (DAG)
  of dependencies.

Release 1.0.5 (2023-08-14)
==========================

* Use ``os.PathLike`` over ``pathlib.Path``

Release 1.0.4 (2023-08-09)
==========================

* Fix tests for Sphinx 7.1 and below

Release 1.0.3 (2023-08-07)
=========================

* Drop support for Python 3.5, 3.6, 3.7, and 3.8
* Raise minimum required Sphinx version to 5.0

Release 1.0.2 (2019-02-29)
==========================

* Fix package metadata has broken

Release 1.0.1 (2019-02-15)
==========================

* Fix release package does not contain locale files

Release 1.0.0 (2019-01-20)
==========================

* Initial release (copied from sphinx package)
