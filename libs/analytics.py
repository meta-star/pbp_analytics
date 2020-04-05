import ipaddress
import json
import sys
from configparser import ConfigParser
from hashlib import sha256
from urllib.parse import urlparse

import requests
import validators
from url_normalize import url_normalize

from .callback import WebServer
from .cron import Cron
from .data import Data
from .initialize import Initialize
from .survey import View, GoogleSafeBrowsing, PhishTank
from .tools import Tools

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
        Initialize(self)
        # Initialization
        self.data_control = Data(self)
        self.view_survey = View(self)
        self.cron_job = Cron(self)
        self.safe_browsing = GoogleSafeBrowsing(
            self.cfg["Google Safe Browsing"]["google_api_key"]
        )
        self.phishtank = PhishTank(
            self.cfg["PhishTank"]["username"],
            self.cfg["PhishTank"]["api_key"]
        )
        Tools.set_ready(False)
        self.cron_job.start()

    def start(self, port: int = 2020):
        """
        Start to listen online
        :return:
        """
        server = WebServer(self)
        while not Tools.check_ready():
            pass
        print(
            Tools.get_time(),
            "[Start] Listening WebServer on port {}".format(port)
        )
        server.listen(port)

    def test(self):
        """

        :return:
        """
        pass

    def stop(self):
        """

        :return:
        """
        self.cron_job.stop()
        sys.exit(0)

    async def server_response(self, message: str):
        try:
            req_res = json.loads(message)
        except json.decoder.JSONDecodeError:
            return {"status": 401}
        if req_res.get("version") is not None:
            try:
                return await self._server_response(req_res)
            except KeyboardInterrupt:
                self.stop()
            except:
                error_report = Tools.error_report()
                Tools.logger(error_report)
                return {"status": 500}
        return {"status": 400}

    async def _server_response(self, data: dict):
        """

        :param data:
        :return:
        """
        if data.get("version") < 1:
            return {
                "status": 505
            }

        if "url" in data and validators.url(data["url"]):
            return await self.analytics(data)

        return {
            "status": 401
        }

    async def analytics(self, data: dict):
        """

        :param data:
        :return:
        """
        url = url_normalize(data.get("url"))
        url_hash = sha256(url.encode("utf-8")).hexdigest()

        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError as e:
            return {
                "status": 403,
                "reason": str(e)
            }

        if response.status_code != 200:
            return {
                "status": 404,
                "http_code": response.status_code
            }

        if "text/html" not in response.headers["content-type"]:
            return {
                "status": 405
            }

        url = response.url

        host = urlparse(url).hostname
        if (validators.ipv4(host) or validators.ipv6(host)) and ipaddress.ip_address(host).is_private:
            return {
                "status": 403,
                "reason": "forbidden"
            }

        cache = self.data_control.find_result_cache_by_url_hash(url_hash)

        if cache is not None:
            score = cache

        elif self.data_control.check_trustlist(url):
            score = 1

        elif self.data_control.check_trust_domain(host):
            score = 1

        elif self.data_control.check_blacklist(url):
            score = 0

        elif self.data_control.check_warnlist(url):
            score = 0.5

        elif self.safe_browsing.lookup([url]):
            score = 0
            self.data_control.mark_as_blacklist(url)

        else:
            score = await self._analytics_inside(data, url)

        if cache is None:
            self.data_control.upload_result_cache(url_hash, score)

        return {
            "status": 200,
            "url": url,
            "trust_score": score
        }

    async def _analytics_inside(self, data: dict, url: str):
        """

        :param data:
        :param url:
        :return:
        """
        if "type" in data:
            target_type = data.get("type")
        else:
            target_type = 0

        origin_urls = []
        async for origin_url in self.view_survey.analytics(target_type, url):
            if origin_url:
                origin_urls.append(origin_url)

        if origin_urls:
            origin_urls_json = json.dumps(origin_urls)
            self.data_control.mark_as_warnlist(url, origin_urls_json)
            return 0.5
        return 1

    async def gen_sample(self):
        """

        :return:
        """
        await self.view_survey.generate()

    def update_blacklist_from_phishtank(self):
        try:
            blacklist = self.phishtank.get_database()
        except OSError:
            print(Tools.get_time(), "[Notice] PhishTank forbidden temporary.")
            return
        for target in blacklist:
            if not self.data_control.check_blacklist(target.get("url")):
                self.data_control.mark_as_blacklist(target.get("url"))
