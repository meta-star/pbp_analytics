import http.client
import sys
import json
import time
from configparser import ConfigParser
from multiprocessing import Process, Queue

import urllib3
import validators
from url_normalize import url_normalize

from .callback import WebServer
from .data import Data
from .initialize import Initialize
from .survey import GoogleSafeBrowsing, View

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
        Initialize(self)
        # Initialization
        http.client._MAXHEADERS = 1000
        self.view_survey = View(self)
        self.data_control = Data(self)
        self.safe_browsing = GoogleSafeBrowsing(
            self.cfg["Google Safe Browsing"]["google_api_key"]
        )
        self.web_agent = urllib3.PoolManager()

    def start(self):
        """
        Start to listen online
        :return:
        """
        server = WebServer(self)
        server.listen()

    def test(self):
        """

        :return:
        """
        pass

    def stop(self):
        """

        :return:
        """
        time.sleep(0.5)
        self.view_survey.close()
        sys.exit(0)

    def server_response(self, message):
        try:
            req_res = json.loads(message)
        except json.decoder.JSONDecodeError:
            return {"status": 401}
        if req_res.get("version") is not None:
            try:
                return await self._server_response(req_res)
            except:
                return {"status": 500}
        return {"status": 400}

    async def _server_response(self, data):
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
                "status": 202
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
            "url": url,
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

        if "type" in data:
            target_type = data.get("type")
        else:
            target_type = 0

        def _origin_check(origin):
            origin_scores.put(
                1
            )

        async for origin_url in self.view_survey.analytics(target_type, url):
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
        await self.view_survey.generate()
