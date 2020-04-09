# Phishing Blocker Project - Analytics

![License](https://img.shields.io/badge/license-MPL--2.0-FF6600.svg) ![Python](https://img.shields.io/badge/python-3.7-0066FF.svg) [![Scrutinizer-CI_Quality](https://scrutinizer-ci.com/g/star-inc/pbp-analytics/badges/quality-score.png?b=master) ![Scrutinizer-CI_Build](https://scrutinizer-ci.com/g/star-inc/pbp-analytics/badges/build.png?b=master)](https://scrutinizer-ci.com/g/star-inc/pbp-analytics/)

The server side of PB Project that analyze URLs with `PageView Technology` which by `structural similarity index`.

![Logo](logo.svg)

## License

This OSS(Open Source Software) is licensed under [Mozilla Public License 2.0](LICENSE.md).

## Database required

`Analytics` using [MySQL](https://www.mysql.com/) or [MariaDB](https://mariadb.org/) as its data driver.

Install one of them, and create a database with any name you like, then import [initialize.sql](initialize.sql) to the database.

Filling the information for connect to the database into `config.ini` as [config.sample.ini](config.sample.ini) did.

## Development

For improving and researching on the platform.

### Requirement

    Ubuntu >= 18.04
    python == 3.7
    pip >= 19.2

### Installation

- Configure `config.ini` at first.

- Follow these commands:

        python3.7 -m pip install requirements.txt
        python3.7 main.py

Enjoy for using and developing.

## Production

In order to security reason, ought not to using without [docker](https://docker.io) for decreasing danger on the host server.

### Installation

- Configure `config.ini` at first.

- Follow these commands:

        sudo docker build -t pbpa .
        sudo docker run --network=host --detach pbpa
  
It should be work.

> (c) 2020 Star Inc.
