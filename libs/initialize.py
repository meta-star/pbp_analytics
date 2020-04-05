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

    config_type = {
        "WebCapture": [
            "capture_type",
            "cache_path",
            "capture_browser"
        ],
        "MySQL": [
            "host",
            "user",
            "passwd",
            "database"
        ],
        "Google Safe Browsing": [
            "google_api_key"
        ],
        "PhishTank": [
            "username",
            "api_key"
        ]
    }

    mysql = [

    ]

    def __init__(self, pbp_handle):
        self.handle = pbp_handle
        self.__config_checker()

    def __config_checker(self):
        for item in self.config_type:
            assert item in self.handle.cfg
            for item_ in self.config_type.get(item):
                assert item_ in self.handle.cfg[item]
        return self.__mysql_checker()

    def __mysql_checker(self):
        pass

    def __mysql_checker_initialize(self):
        pass

    def __mysql_checker_repair(self):
        pass
