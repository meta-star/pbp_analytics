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

import libs.callback as callback


class PBP:
    def __init__(self):
        self.WebCapture = None
        self.cfg = ConfigParser()
        self.cfg.read("config.ini")

    @staticmethod
    def getTime(time_format="%b %d %Y %H:%M:%S %Z"):
        time_ = time.localtime(time.time())
        return time.strftime(time_format, time_)

    def view_compare(self):
        pass

    def rank(self):
        pass

    def start(self):
        mp.Process(target=callback.listen, args=(0,)).start()


if __name__ == "__main__":
    handle = PBP()
    print("PBP Server\n{}\n".format(handle.getTime()))
    handle.start()
