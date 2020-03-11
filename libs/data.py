import mysql.connector as sql_client

"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


class Data:
    """
    To control data for PBP
    """
    def __init__(self, db_connect_info):
        """
        Configure and initialize database details
        :param db_connect_info:
        """
        self.db_client = sql_client.connect(**db_connect_info)

    def insert(self):
        pass

    def update(self):
        pass

    def query(self):
        pass
