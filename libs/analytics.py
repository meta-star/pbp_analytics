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
    Copyright (c) 2020 Star Inc.(https://starinc.xyz)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


class Analytics:
    # Loading Configs
    cfg = {}

    def __init__(self, config: str):
        # Read Config
        if config == "ENV":
            self.config = config
        else:
            self.config = ConfigParser()
            self.config.read(config)
        # Initialization
        Initialize(self)
        self.data_control = Data(self)
        self.view_survey = View(self)
        self.cron_job = Cron(self)
        self.safe_browsing = GoogleSafeBrowsing(
            self.cfg["SafeBrowsing"]["google_api_key"]
        )
        self.phishtank = PhishTank(
            self.cfg["PhishTank"]["username"],
            self.cfg["PhishTank"]["api_key"]
        )
        Tools.set_ready(False)

    def start(self, port: int = 2020):
        """
        Start web service

        :param port: integer of port to listen online
        :return:
        """
        try:
            server = WebServer(self)
            self.cron_job.start()
            while not Tools.check_ready():
                pass
            print(
                Tools.get_time(),
                "[Start] Listening WebServer on port {}".format(port)
            )
            server.listen(port)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """
        Shutdown web service

        :return:
        """
        self.cron_job.stop()
        sys.exit(0)

    async def analyze(self, data: dict):
        """
        Do analysis from URL sent by message with databases

        :param data: dict from message decoded
        :return: dict to response
        """
        url = url_normalize(data.get("url"))
        url_hash = sha256(url.encode("utf-8")).hexdigest()

        result_from_db = await self.check_from_database(url, url_hash, urlparse(url).hostname)
        if check_from_database is not result_from_db:
            return {
                "status": 200,
                "url": url,
                "trust_score": result_from_db
            }

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

        host = urlparse(url).hostname if urlparse(
            url
        ).hostname != "localhost" else "127.0.0.1"

        if (validators.ipv4(host) or validators.ipv6(host)) and \
                ipaddress.ip_address(host).is_private:
            return {
                "status": 403,
                "reason": "forbidden"
            }

        return {
            "status": 200,
            "url": url,
            "trust_score": await self._deep_analyze(url)
        }

    async def check_from_database(self, url: str, url_hash: str, host: str):
        """
        Check URL whether existed in database

        :param url: URL from request
        :param url_hash: URL hashed
        :param host: host from URL decoded
        :return: trust_score or NoneType
        """
        cache = self.data_control.find_result_cache_by_url_hash(url_hash)

        if cache is not None:
            score = cache

        elif self.data_control.check_trustlist(url) or \
                self.data_control.check_trust_domain(host):
            score = 1

        elif self.data_control.check_warnlist(url):
            score = 0.5

        elif self.data_control.check_blacklist(url):
            score = 0

        elif self.safe_browsing.lookup([url]):
            self.data_control.mark_as_blacklist(url)
            score = 0

        else:
            return None

        if cache is None:
            self.data_control.upload_result_cache(url_hash, score)

        return score

    async def _deep_analyze(self, url: str):
        """
        Analyze URL with PageView

        :param url: URL that latest get via `requests`
        :return: float of the-trust-score between 0 to 1
        """
        origin_urls = []
        async for origin_url in self.view_survey.analyze(url):
            if origin_url:
                origin_urls.append(origin_url)

        if origin_urls:
            origin_urls_json = json.dumps(origin_urls)
            self.data_control.mark_as_warnlist(url, origin_urls_json)
            return 0.5
        return 1

    async def gen_sample(self):
        """
        Generate PageView samples with trustlist

        :return:
        """
        await self.view_survey.generate()

    def update_blacklist_from_phishtank(self):
        """
        Update database for blacklist from PhishTank

        :return:
        """
        try:
            blacklist = self.phishtank.get_database()
        except OSError:
            print(Tools.get_time(), "[Notice] PhishTank forbidden temporary.")
            return

        self.data_control.mark_as_blacklist_mass(
            [target.get("url") for target in blacklist]
        )
