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
        self.pbp_handle = pbp_handle
        self.db_client = sql_client.connect(**pbp_handle.cfg["MySQL"])

    @mysql_checker
    def check_trustlist(self, url: str):
        """

        :param url:
        :return:
        """
        cursor = self.db_client.cursor(dictionary=True)
        cursor.execute(
            "SELECT `uuid` FROM `trustlist` WHERE `url` = %s",
            (url,)
        )
        result = cursor.fetchall()
        self.db_client.commit()
        cursor.close()
        if result:
            return result[0]

    @mysql_checker
    def check_trust_domain(self, domain: str):
        """

        :param domain:
        :return:
        """
        cursor = self.db_client.cursor(dictionary=True)
        cursor.execute(
            "SELECT `uuid` FROM `trust_domain` WHERE `domain` = %s",
            (domain,)
        )
        result = cursor.fetchall()
        self.db_client.commit()
        cursor.close()
        if result:
            return result[0]

    @mysql_checker
    def check_blacklist(self, url: str):
        """

        :param url:
        :return:
        """
        cursor = self.db_client.cursor(dictionary=True)
        cursor.execute(
            "SELECT `url`, `date` FROM `blacklist` WHERE `url` = %s",
            (url,)
        )
        result = cursor.fetchall()
        self.db_client.commit()
        cursor.close()
        if result:
            return result[0]

    @mysql_checker
    def check_warnlist(self, url: str):
        """

        :param url:
        :return:
        """
        cursor = self.db_client.cursor(dictionary=True)
        cursor.execute(
            "SELECT `url`, `origin`, `date` FROM `warnlist` WHERE `url` = %s",
            (url,)
        )
        result = cursor.fetchall()
        self.db_client.commit()
        cursor.close()
        if result:
            return result[0]

    @mysql_checker
    def get_urls_from_trustlist(self):
        """

        :return:
        """
        cursor = self.db_client.cursor()
        cursor.execute(
            "SELECT `url` FROM `trustlist`"
        )
        result = cursor.fetchall()
        self.db_client.commit()
        cursor.close()
        if result:
            return [record[0] for record in result]
        return []

    @mysql_checker
    def get_view_narray_from_trustlist(self):
        """

        :return:
        """
        cursor = self.db_client.cursor(dictionary=True)
        cursor.execute(
            "SELECT `url`, `target_view_narray` FROM `trustlist`"
        )
        result = cursor.fetchall()
        self.db_client.commit()
        cursor.close()
        return result

    @mysql_checker
    def get_view_narray_from_trustlist_with_target_type(self, target_type: int):
        """

        :param target_type:
        :return:
        """
        cursor = self.db_client.cursor(dictionary=True)
        cursor.execute(
            "SELECT `url`, `target_view_narray` FROM `trustlist` WHERE `type` = %s",
            (target_type,)
        )
        result = cursor.fetchall()
        self.db_client.commit()
        cursor.close()
        return result

    @mysql_checker
    def find_page_by_view_signature(self, signature: str):
        """

        :param signature:
        :return:
        """
        cursor = self.db_client.cursor()
        cursor.execute(
            "SELECT `url` FROM `trustlist` WHERE `target_view_signature` = %s",
            (signature,)
        )
        result = cursor.fetchall()
        self.db_client.commit()
        cursor.close()
        if result:
            return result[0][0]
        return None

    @mysql_checker
    def find_result_cache_by_url_hash(self, url_hash: str):
        """

        :param url_hash:
        :return:
        """
        cursor = self.db_client.cursor()
        cursor.execute(
            "SELECT `score` FROM `result_cache` WHERE `url_hash` = %s",
            (url_hash,)
        )
        result = cursor.fetchall()
        self.db_client.commit()
        cursor.close()
        if result:
            return result[0][0]
        return None

    @mysql_checker
    def upload_result_cache(self, url_hash: str, score: float):
        """

        :param url_hash:
        :param score:
        :return:
        """
        cursor = self.db_client.cursor()
        cursor.execute(
            "INSERT INTO `result_cache`(`url_hash`, `score`) VALUES (%s, %s)",
            (url_hash, score)
        )
        self.db_client.commit()
        cursor.close()
        return True

    @mysql_checker
    def clean_result_cache(self):
        """

        :return:
        """
        cursor = self.db_client.cursor()
        cursor.execute("TRUNCATE TABLE `result_cache`")
        self.db_client.commit()
        cursor.close()
        return True

    @mysql_checker
    def upload_view_sample(self, url: str, view_signature: str, view_data: str):
        """

        :param url:
        :param view_signature:
        :param view_data:
        :return:
        """
        cursor = self.db_client.cursor()
        if self.check_trustlist(url):
            cursor.execute(
                "UPDATE `trustlist` SET `target_view_signature` = %s, `target_view_narray` = %s WHERE `url` = %s",
                (view_signature, view_data, url)
            )
        else:
            cursor.execute(
                "INSERT INTO `trustlist`(`url`, `target_view_signature`, `target_view_narray`) VALUES (%s, %s, %s)",
                (url, view_signature, view_data)
            )
        self.db_client.commit()
        cursor.close()
        return True

    @mysql_checker
    def mark_as_blacklist(self, url: str):
        """

        :param url:
        :return:
        """
        cursor = self.db_client.cursor()
        cursor.execute(
            "INSERT INTO `blacklist`(`url`, `date`) VALUES (%s, NOW())",
            (url,)
        )
        self.db_client.commit()
        cursor.close()
        return True

    @mysql_checker
    def mark_as_warnlist(self, url: str, origin_url: str):
        """

        :param origin_url:
        :param url:
        :return:
        """
        cursor = self.db_client.cursor()
        cursor.execute(
            "INSERT INTO `warnlist`(`url`, `origin`, `date`) VALUES (%s, %s, NOW())",
            (url, origin_url)
        )
        self.db_client.commit()
        cursor.close()
        return True
