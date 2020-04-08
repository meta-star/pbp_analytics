import mysql.connector as sql_client

from .tools import Tools

"""
    Copyright (c) 2020 Star Inc.(https://starinc.xyz)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


class Initialize:
    print("""
    Phishing Blocker Project - Analytics
    
    Copyright (c) 2020 Star Inc.(https://starinc.xyz)
    
    Now: {}
    ===
        This OSS is licensed under the Mozilla Public License, v. 2.0.
        Source Code: https://github.com/star-inc/pbp-analytics
    ===
    """.format(Tools.get_time()))

    default_configs = {
        "WebCapture": {
            "capture_type": "2",
            "cache_path": "./cache/",
            "capture_browser": "firefox"
        },
        "MySQL": {
            "host": "localhost",
            "user": None,
            "passwd": None,
            "database": None
        },
        "Google Safe Browsing": {
            "google_api_key": None
        },
        "PhishTank": {
            "username": None,
            "api_key": None
        }
    }

    mysql_tables = [
        "blacklist",
        "result_cache",
        "trustlist",
        "trust_domain",
        "warnlist"
    ]

    def __init__(self, pbp_handle):
        """
        Load configs and databases from config.ini
        :param pbp_handle: Analytics object
        """
        self.handle = pbp_handle
        self.__config_checker()

    def __config_checker(self):
        """
        Check configs
        :return:
        """
        self.handle.cfg = self.default_configs
        for item in self.default_configs:
            for item_ in self.default_configs.get(item):
                if item in self.handle.config and item_ in self.handle.config[item]:
                    self.handle.cfg[item][item_] = self.handle.config[item][item_]
                else:
                    self.handle.cfg[item][item_] = self.default_configs[item][item_]
                assert self.handle.cfg[item][item_] is not None, \
                    "{}/{} is not found in config.ini".format(item, item_)
        return self.__mysql_checker()

    def __mysql_checker(self):
        """
        Check databases simply
        :return:
        """
        client = sql_client.connect(**self.handle.cfg["MySQL"])

        def check_table_exists(table: str):
            """
            To check table whether exists in database
            :param table: name of table
            :return: bool
            """
            cursor = client.cursor(dictionary=True)
            cursor.execute("SHOW TABLES LIKE %s", (table,))
            result = cursor.fetchall()
            client.commit()
            cursor.close()
            if result:
                return True
            return False

        for item in self.mysql_tables:
            assert check_table_exists(item), \
                "Table {} does not exists in database".format(item)
