from functools import wraps
from typing import Callable

import aiomysql

"""
    Copyright (c) 2020 Star Inc.(https://starinc.xyz)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


def mysql_checker(function):
    """
    To wrap a function for preventing to disconnect from the database
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            result = args[0].connect(function, (args, kwargs,))
            args[0].db_error_checkpoint = 0
            return result
        except aiomysql.OperationalError:
            if args[0].db_error_checkpoint:
                assert "sql_error"
            args[0].db_error_checkpoint = 1
            return function(*args)

    return wrapper


class Data:
    """
    To control MySQL for PBP

    Attributes
    -----------
    handle: Analytics object
    """

    db_error_checkpoint = 0

    def __init__(self, pbp_handle):
        self.handle = pbp_handle

    async def connect(self, function: Callable, *args, **kwargs):
        pool = await aiomysql.create_pool(**self.handle.cfg["MySQL"])
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                function(cur, *args, **kwargs)
        pool.close()
        await pool.wait_closed()

    @mysql_checker
    def check_trustlist(self, cursor: aiomysql.cursors, url: str):
        """
        To check URL whether exists in trustlist

        :param url: URL
        :param cursor:
        :return: string of UUID or NoneType
        """
        cursor.execute(
            "SELECT `uuid` FROM `trustlist` WHERE `url` = %s",
            (url,)
        )
        result = cursor.fetchall()
        if result:
            return result[0]

    @mysql_checker
    def check_trust_domain(self, cursor: aiomysql.cursors, domain: str):
        """
        To check URL whether exists in trust_domain list

        :param domain: domain
        :return: string of UUID or NoneType
        """
        cursor.execute(
            "SELECT `uuid` FROM `trust_domain` WHERE `domain` = %s",
            (domain,)
        )
        result = cursor.fetchall()
        if result:
            return result[0]

    @mysql_checker
    def check_blacklist(self, cursor: aiomysql.cursors, url: str):
        """
        To check URL whether exists in blacklist

        :param url: URL
        :return: dict of URL and Mark-Date or NoneType
        """
        cursor.execute(
            "SELECT `url`, `date` FROM `blacklist` WHERE `url` = %s",
            (url,)
        )
        result = cursor.fetchall()
        if result:
            return result[0]

    @mysql_checker
    def check_warnlist(self, cursor: aiomysql.cursors, url: str):
        """
        To check URL whether exists in warnlist

        :param url: URL
        :return: dict of URL, similar URL and Mark-Date or NoneType
        """
        cursor.execute(
            "SELECT `url`, `origin`, `date` FROM `warnlist` WHERE `url` = %s",
            (url,)
        )
        result = cursor.fetchall()
        if result:
            return result[0]

    @mysql_checker
    def get_urls_from_trustlist(self, cursor: aiomysql.cursors):
        """
        Fetch all URL in trustlist

        :return: list of URL
        """
        cursor.execute(
            "SELECT `url` FROM `trustlist`"
        )
        result = cursor.fetchall()
        if result:
            return [record[0] for record in result]
        return []

    @mysql_checker
    def get_view_narray_from_trustlist(self, cursor: aiomysql.cursors):
        """
        Fetch all target_view_narray in trustlist

        :return: dict of URL and NumPy Array
        """
        cursor.execute(
            "SELECT `url`, `target_view_narray` FROM `trustlist`"
        )
        result = cursor.fetchall()
        return result

    @mysql_checker
    def find_page_by_view_signature(self, cursor: aiomysql.cursors, signature: str):
        """
        Search URL by view_signature in trustlist

        :param signature: string hashed
        :return: URL or NoneType
        """
        cursor.execute(
            "SELECT `url` FROM `trustlist` WHERE `target_view_signature` = %s",
            (signature,)
        )
        result = cursor.fetchall()
        if result:
            return result[0][0]
        return None

    @mysql_checker
    def find_result_cache_by_url_hash(self, cursor: aiomysql.cursors, url_hash: str):
        """
        Search cache by url_hash in result_cache

        :param url_hash: URL hashed
        :return: float of the-trust-score or NoneType
        """
        cursor.execute(
            "SELECT `score` FROM `result_cache` WHERE `url_hash` = %s",
            (url_hash,)
        )
        result = cursor.fetchall()
        if result:
            return result[0][0]
        return None

    @mysql_checker
    def upload_result_cache(self, cursor: aiomysql.cursors, url_hash: str, score: float):
        """
        Upload the-trust-score to cache

        :param url_hash: URL hashed
        :param score: float of the-trust-score
        :return:
        """
        cursor.execute(
            "INSERT INTO `result_cache`(`url_hash`, `score`) VALUES (%s, %s)",
            (url_hash, score)
        )
        return True

    @mysql_checker
    def clean_result_cache(self, cursor: aiomysql.cursors):
        """
        Clean result caches

        :return: True
        """
        cursor.execute("TRUNCATE TABLE `result_cache`")
        return True

    @mysql_checker
    def upload_view_sample(self, cursor: aiomysql.cursors, url: str, view_signature: str, view_data: str):
        """
        Upload ViewSample for PageView

        :param url: URL of Sample
        :param view_signature: string hashed with view_data
        :param view_data: string of num array base64 encoded
        :return: True
        """
        if self.check_trustlist(url):
            cursor.execute(
                "UPDATE `trustlist` SET `target_view_signature` = %s, `target_view_narray` = %s WHERE `url` = %s",
                (view_signature, view_data, url)
            )
        else:
            cursor.execute(
                "INSERT INTO "
                "`trustlist`(`uuid`, `url`, `target_view_signature`, `target_view_narray`) "
                "VALUES (UUID(), %s, %s, %s)",
                (url, view_signature, view_data)
            )
        return True

    @mysql_checker
    def mark_as_blacklist(self, cursor: aiomysql.cursors, url: str):
        """
        Mark URL to blacklist by Database

        :param url: URL to mark
        :return: True
        """
        cursor.execute(
            "INSERT INTO `blacklist`(`uuid`, `url`, `date`) VALUES (UUID(), %s, NOW())",
            (url,)
        )
        return True

    @mysql_checker
    def mark_as_warnlist(self, cursor: aiomysql.cursors, url: str, origin_url: str):
        """
        Mark URL to warnlist by PageView

        :param url: URL to mark
        :param origin_url: the URL similar to
        :return: True
        """
        cursor.execute(
            "INSERT INTO `warnlist`(`uuid`, `url`, `origin`, `date`) VALUES (UUID(), %s, %s, NOW())",
            (url, origin_url)
        )
        return True
