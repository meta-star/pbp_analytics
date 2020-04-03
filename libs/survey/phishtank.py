import gzip
import json

import requests

"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


class PhishTank:
    """
    OpenDNS PhishTank Client
    https://www.phishtank.com/
    """

    def __init__(self, username: str, api_key: str):
        """
        Initialization
        :param username: PhishTank Username
        :param api_key: PhishTank API Key
        """
        self.username = username
        self.api_key = api_key

        self.api_url = "https://checkurl.phishtank.com/checkurl/"
        self.db_url = "http://data.phishtank.com/data/{}/online-valid.json.gz".format(api_key)

    def lookup(self, url: str):
        """
        To check URLs from PhishTank
        :param url: URL
        :return: dict
        """
        header = {"user-agent": "phishtank/{}".format(self.username)}

        query_data = {
            "url": url,
            "format": "json",
            "app_key": self.api_key
        }

        return requests.post(self.api_url, headers=header, params=query_data)

    def get_database(self):
        """
        Get database from PhishTank
        :return: dict
        """
        data = requests.get(self.db_url)
        decompressed_data = gzip.decompress(data.content)
        return json.loads(decompressed_data)
