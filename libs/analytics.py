import http.client
import sys
import time
import traceback
from configparser import ConfigParser
from multiprocessing import Process, Queue

import urllib3
import validators
from url_normalize import url_normalize

from .callback import WebServer
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

    hour_cache = {}

    def __init__(self):
        self.__config_checker()
        # Initialization
        http.client._MAXHEADERS = 1000
        self.data_control = Data(self)
        self.safe_browsing = GoogleSafeBrowsing(
            self.cfg["Google Safe Browsing"]["google_api_key"]
        )
        self.web_agent = urllib3.PoolManager()
        self.target_handle = Target(self)
        self.origin_handle = Origin(self)

    def start(self):
        """

        :return:
        """
        server = WebServer(self)
        server.listen()

    def stop(self):
        """

        :return:
        """
        time.sleep(0.5)
        self.target_handle.close()
        sys.exit(0)

    @staticmethod
    def __config_checker():
        assert 1 == 1

    @staticmethod
    def get_time(time_format="%b %d %Y %H:%M:%S %Z"):
        """

        :param time_format:
        :return:
        """
        time_ = time.localtime(time.time())
        return time.strftime(time_format, time_)

    @staticmethod
    def error_report():
        """
        Report errors as tuple
        :return: tuple
        """
        _, _, err3 = sys.exc_info()
        traceback.print_tb(err3)
        tb_info = traceback.extract_tb(err3)
        filename, line, _, text = tb_info[-1]
        error_info = "occurred in\n{}\n\non line {}\nin statement {}".format(filename, line, text)
        return error_info

    async def server_response(self, data):
        """

        :param data:
        :return:
        """
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
            return await self.analytics(data)

        return {
            "status": 401
        }

    async def analytics(self, data):
        """

        :param data:
        :return:
        """
        url = url_normalize(data.get("url"))

        try:
            response = self.web_agent.request('GET', url)
        except urllib3.exceptions.MaxRetryError as e:
            return {
                "status": 403,
                "reason": str(e.reason)
            }

        if response.status != 200:
            return {
                "status": 404,
                "http_code": response.status
            }

        if self.data_control.check_trustlist(url):
            score = 1

        elif self.data_control.check_blacklist(url):
            score = 0

        elif self.safe_browsing.lookup([url]):
            score = 0
            self.data_control.mark_as_blacklist(url)

        elif url in self.hour_cache:
            score = self.hour_cache[url]

        else:
            score = await self._analytics_inside(data, url)
            self.hour_cache[url] = score

        return {
            "status": 200,
            "trust_score": score
        }

    async def _analytics_inside(self, data, url):
        """

        :param data:
        :param url:
        :return:
        """
        origin_scores = Queue()
        thread = None
        data_num = 0

        def _origin_check(origin):
            origin_scores.put(
                self.origin_handle.action(origin, url)
            )

        async for origin_url in self.target_handle.analytics(data, url):
            thread = Process(
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

        if results and max(results) < 0.5:
            self.data_control.mark_as_blacklist(url)
            return 0

        return 1

    async def gen_sample(self):
        """

        :return:
        """
        await self.target_handle.generate()
        self.origin_handle.generate()
