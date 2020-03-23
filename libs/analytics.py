import sys
import time
from configparser import ConfigParser

import validators
from url_normalize import url_normalize

from .callback import HttpServer
from .comparer.origin import OriginAnalytics
from .comparer.target import TargetAnalytics
from .data import Data
from .safebrowsing import GoogleSafeBrowsing

"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


class Analytics:
    # Loading Configs
    cfg = ConfigParser()
    cfg.read("config.ini")

    def __init__(self):
        # Initialization
        self.data_control = Data(self)
        self.safe_browsing = GoogleSafeBrowsing(
            self.cfg["Google Safe Browsing"]["google_api_key"]
        )
        self.target_analytics = TargetAnalytics(self)
        self.origin_analytics = OriginAnalytics(self)

    @staticmethod
    def get_time(time_format="%b %d %Y %H:%M:%S %Z"):
        time_ = time.localtime(time.time())
        return time.strftime(time_format, time_)

    def start(self):
        server = HttpServer(self)
        server.listen()

    @staticmethod
    def stop():
        time.sleep(0.5)
        sys.exit(0)

    def analytics(self, data):
        if data.get("version") < 1:
            return {
                "status": 505
            }
        if data.get("shutdown"):
            self.stop()
            return {
                "status": 200
            }
        elif data.get("url") and validators.url(data.get("url")):
            url = url_normalize(data.get("url"))

            score = 1

            if self.data_control.check_blacklist(url):
                pass

            elif self.data_control.check_blacklist(url):
                score = 0

            elif self.safe_browsing.lookup([url]):
                score = 0
                self.data_control.mark_as_blacklist(url)

            # elif self.target_analytics.action(url) > 0.5:
            #    if self.origin_analytics.action(url) < 0.5:
            #        self.data_control.mark_as_blacklist(url)
            #        score = 0

            return {
                "status": 200,
                "trust-score": score
            }
        return {
            "status": 401
        }

    def gen_sample(self):
        pass
