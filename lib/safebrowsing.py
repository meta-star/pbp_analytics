import requests
"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


class GoogleSafeBrowsing:
    def __init__(self, google_api_key):

        host = "safebrowsing.googleapis.com"

        api_ver = "v4"

        lookup_path = "threatMatches:find"
        update_path = "threatListUpdates:fetch"

        self.lookup_url = "https://{}/{}/{}?key={}".format(host, api_ver, lookup_path, google_api_key)
        self.update_url = "https://{}/{}/{}?key={}".format(host, api_ver, update_path, google_api_key)

    def lookup(self, urls):
        query_urls = [{"url": url} for url in urls]

        query_data = {
            "client": {
                "clientId": "PhishingBlock Project",
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

