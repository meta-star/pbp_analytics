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

    def __init__(self, pbp_handle):
        """
        Configure and initialize database details
        :param pbp_handle:
        """
        self.db_client = sql_client.connect(**pbp_handle.cfg["MySQL"])

        self.pbp_handle = pbp_handle

    def check_blacklist(self, url):
        cursor = self.db_client.cursor(dictionary=True)
        cursor.execute(
            "SELECT `url`, `date` FROM blacklist WHERE url = %s",
            (url,)
        )
        result = cursor.fetchall()
        self.db_client.commit()
        cursor.close()
        return result

    def mark_as_blacklist(self, url):
        cursor = self.db_client.cursor()
        date = self.pbp_handle.get_time("%Y-%m-%d ")
        cursor.execute(
            "INSERT INTO `blacklist`(`url`, `date`) VALUES (%s, %s)",
            (url, date)
        )
        self.db_client.commit()
        cursor.close()
        return True

    def find_page_view_signature(self, sign):
        cursor = self.db_client.cursor(dictionary=True)
        cursor.execute(
            "SELECT `url, date, data` FROM view_signatures WHERE signature = %s",
            (sign,)
        )
        result = cursor.fetchall()
        self.db_client.commit()
        cursor.close()
        return result
