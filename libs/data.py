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

    def check_blacklist(self, url):
        cursor = self.db_client.cursor(dictionary=True)
        cursor.execute(
            "SELECT `url`, `date`, `data` FROM blacklist WHERE url = %s",
            (url,)
        )
        result = cursor.fetchall()
        self.db_client.commit()
        cursor.close()
        return result

    def find_page_view_signature(self, sign):
        with self.db_client.cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT `url, date, data` FROM view_signatures WHERE signature = %s",
                (sign,)
            )
            self.db_client.commit()
            return cursor.fetchall()
