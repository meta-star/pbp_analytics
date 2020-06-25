Installation
============

Database required
-----------------

`Analytics` using MySQL_ or MariaDB_ as its data driver.

Install one of them, and create a database with any name you like, then import initialize.sql_ to the database.

Filling the information for connect to the database into `config.ini` as config.sample.ini_ did.

.. _MySQL: https://www.mysql.com/
.. _MariaDB: https://mariadb.org/
.. _initialize.sql: https://github.com/star-inc/pbp-analytics/blob/master/initialize.sql
.. _config.sample.ini: https://github.com/star-inc/pbp-analytics/blob/master/config.sample.ini

Selections
----------

.. toctree::
   :maxdepth: 2
   :caption: Select

   production
   development
