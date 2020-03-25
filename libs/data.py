import mysql.connector as sql_client

"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


def mysql_checker(function):
    def wrapper(*args, **kwargs):
        try:
            result = function(*args, **kwargs)
            args[0].db_error_checkpoint = 0
            return result
        except sql_client.errors.OperationalError:
            if args[0].db_error_checkpoint:
                assert "sql_error"
            args[0].db_error_checkpoint = 1
            args[0].__init__(args[0].pbp_handle)
            return function(*args)

    return wrapper


class Data:
    """
    To control data for PBP
    """

    db_error_checkpoint = 0

    def __init__(self, pbp_handle):
        """
        Configure and initialize database details
        :param pbp_handle:
        """
        self.db_client = sql_client.connect(**pbp_handle.cfg["MySQL"])

        self.pbp_handle = pbp_handle

    @mysql_checker
    def check_trustlist(self, url):
        cursor = self.db_client.cursor(dictionary=True)
        cursor.execute(
            "SELECT `url` FROM `trustlist` WHERE `url` = %s",
            (url,)
        )
        result = cursor.fetchall()
        self.db_client.commit()
        cursor.close()
        return result

    @mysql_checker
    def check_blacklist(self, url):
        cursor = self.db_client.cursor(dictionary=True)
        cursor.execute(
            "SELECT `url`, `date` FROM `blacklist` WHERE `url` = %s",
            (url,)
        )
        result = cursor.fetchall()
        self.db_client.commit()
        cursor.close()
        return result

    @mysql_checker
    def get_urls_from_trustlist(self):
        cursor = self.db_client.cursor()
        cursor.execute(
            "SELECT `url` FROM `trustlist`"
        )
        result = cursor.fetchall()
        self.db_client.commit()
        cursor.close()
        return [record[0] for record in result]

    @mysql_checker
    def find_page_by_view_signature(self, sign):
        cursor = self.db_client.cursor(dictionary=True)
        cursor.execute(
            "SELECT `url` FROM `trustlist` WHERE `target_view_signature` = %s",
            (sign,)
        )
        result = cursor.fetchall()
        self.db_client.commit()
        cursor.close()
        return result

    @mysql_checker
    def upload_view_sample(self, url, view_signature, view_data):
        cursor = self.db_client.cursor()
        if self.check_trustlist(url):
            cursor.execute(
                "UPDATE `trustlist` SET `target_view_signature`=%s, `target_view_narray`=%s WHERE `url`=%s",
                (view_signature, view_data, url)
            )
        else:
            cursor.execute(
                "INSERT INTO `trustlist`(`url`, `target_view_signature`, `target_view_narray`=%s) VALUES (%s, %s, %s)",
                (url, view_signature, view_data)
            )
        self.db_client.commit()
        cursor.close()
        return True

    @mysql_checker
    def mark_as_blacklist(self, url):
        cursor = self.db_client.cursor()
        date = self.pbp_handle.get_time("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO `blacklist`(`url`, `date`) VALUES (%s, %s)",
            (url, date)
        )
        self.db_client.commit()
        cursor.close()
        return True
