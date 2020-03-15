import time
from configparser import ConfigParser

import validators

from . import ThreadControl, HttpServer, Data
from .comparer.origin import DomainResolve

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

    # Initialization
    thread_control = ThreadControl()
    data_control = Data(cfg["MySQL"])

    domain_resolve = DomainResolve()

    analytic_tasks = []

    @staticmethod
    def get_time(time_format="%b %d %Y %H:%M:%S %Z"):
        time_ = time.localtime(time.time())
        return time.strftime(time_format, time_)

    def start(self):
        server = HttpServer(self)
        self.thread_control.add(server.listen, ())

    def stop(self):
        self.thread_control.stop("listen")

    def analytics(self, data):
        if validators.url(data.get("url")):
            if self.data_control.check_blacklist(data.get("url")):
                score = 0
            else:
                for task in self.analytic_tasks:
                    self.thread_control.add(task, (data.get("url"),))
                score = 1
            return {
                "status": 200,
                "trust-score": score
            }
        return {
            "status": 401
        }
