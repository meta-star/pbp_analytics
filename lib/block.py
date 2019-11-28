import mysql.connector as sql_client
"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

class Block:
    def __init__(self):
        self.db_connect_info = {
            "host": "localhost",
            "user": "",
            "passwd": "",
            "database": ""
        }
        self.db_client = sql_client.connect(**self.db_connect_info)

    def queryUrl(self, url):
        return url

    def markUrl(self, url, type):
        pass
