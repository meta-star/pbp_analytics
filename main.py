#!/usr/bin/env python3
"""
PB Project - analytics

(c)2019 SuperSonic(https://randychen.tk).
===
    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
===
"""

import multiprocessing as mp
import time

from configparser import ConfigParser

from libs import callback, Data, WebCapture, ThreadControl


class PBP:
    def __init__(self):
        self.handles = {}

        self.cfg = ConfigParser()
        self.cfg.read("config.ini")

        self.handles["capture"] = WebCapture(self.cfg["WebCapture"])
        self.handles["database"] = Data(self.cfg["MySQL"])

    @staticmethod
    def get_time(time_format="%b %d %Y %H:%M:%S %Z"):
        time_ = time.localtime(time.time())
        return time.strftime(time_format, time_)

    def view_compare(self):
        pass

    def rank(self):
        pass

    def start(self):
        ThreadControl.add(callback.listen, (0,))


if __name__ == "__main__":
    handle = PBP()
    print("PBP Server\n{}\n".format(handle.get_time()))
    handle.start()
