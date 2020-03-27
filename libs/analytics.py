import sys
import time
from configparser import ConfigParser
from queue import Queue
from threading import Thread
from urllib import request

import validators
from url_normalize import url_normalize

from .callback import HttpServer
from .comparer import Origin, Target
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
        self.target_handle = Target(self)
        self.origin_handle = Origin(self)

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
        url = url_normalize(data.get("url"))

        http_status = request.urlopen(url).getcode()
        if http_status != 200:
            return {
                "status": 404,
                "http_code": http_status
            }

        score = 1

        if self.data_control.check_trustlist(url):
            pass

        elif self.data_control.check_blacklist(url):
            score = 0

        elif self.safe_browsing.lookup([url]):
            score = 0
            self.data_control.mark_as_blacklist(url)

        else:
            origin_scores = Queue()
            thread = None
            data_num = 0

            def _origin_check(origin):
                origin_scores.put(
                    self.origin_handle.action(origin, url)
                )

            for origin_url in self.target_handle.analytics(data, url):
                thread = Thread(
                    target=_origin_check,
                    args=(origin_url,)
                )
                thread.start()
                data_num += 1

            if thread:
                thread.join()

            results = []
            for _ in range(data_num):
                results.append(origin_scores.get())

            if origin_scores and max(results) < 0.5:
                self.data_control.mark_as_blacklist(url)
                score = 0

        return {
            "status": 200,
            "trust_score": score
        }

    def server_response(self, data):
        if data.get("version") < 1:
            return {
                "status": 505
            }

        if data.get("shutdown"):
            self.stop()
            return {
                "status": 200
            }
        elif validators.url(data.get("url")):
            return self.analytics(data)

        return {
            "status": 401
        }

    def gen_sample(self):
        self.target_handle.generate()
        self.origin_handle.generate()
