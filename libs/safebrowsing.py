import requests

"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


class GoogleSafeBrowsing:
    """
    Google SafeBrowsing Client
    """

    def __init__(self, google_api_key):
        """
        Initialization
        :param google_api_key: Google API Token
        """
        host = "safebrowsing.googleapis.com"

        api_ver = "v4"

        lookup_path = "threatMatches:find"
        update_path = "threatListUpdates:fetch"

        self.lookup_url = "https://{}/{}/{}?key={}".format(host, api_ver, lookup_path, google_api_key)
        self.update_url = "https://{}/{}/{}?key={}".format(host, api_ver, update_path, google_api_key)

    def lookup(self, urls):
        """
        To check URLs from Google SafeBrowsing
        :param urls: list of URLs
        :return: dict
        """
        query_urls = [{"url": url} for url in urls]

        query_data = {
            "client": {
                "clientId": "Phishing Blocker Project - Analytics",
                "clientVersion": "0.1"
            },
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": query_urls
            }
        }

        return requests.post(self.lookup_url, json=query_data).json()
