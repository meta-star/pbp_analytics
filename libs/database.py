import mysql.connector as sql_client

"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


class DatabaseConnectInfo:
    def to_dict(self):
        return {
            1:1
        }


class Data:
    def __init__(self, db_connect_info):
        self.db_client = sql_client.connect(**db_connect_info.to_dict())

    def image_register(self):
        pass

    def url_query(self, url):
        return url

    def url_mark(self, url, type):
        pass
