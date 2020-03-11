#!/usr/bin/env python3
"""
Phishing Blocker Project - Analytics

(c)2019 SuperSonic(https://randychen.tk).
===
    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
===
"""

import time

from configparser import ConfigParser
from libs import ThreadControl, HttpServer, Data


class PBP:
    # Loading Configs
    cfg = ConfigParser()
    cfg.read("config.ini")

    # Initialization
    thread_control = ThreadControl()
    data_control = Data(**cfg["MySQL"])

    @staticmethod
    def get_time(time_format="%b %d %Y %H:%M:%S %Z"):
        time_ = time.localtime(time.time())
        return time.strftime(time_format, time_)

    def start(self):
        server = HttpServer(self)
        self.thread_control.add(server.listen, ())


if __name__ == "__main__":
    handle = PBP()
    print("PBP Server\n{}\n".format(handle.get_time()))
    handle.start()
