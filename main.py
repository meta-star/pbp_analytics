"""
PB Project - analytics

(c)2019 SuperSonic(https://randychen.tk).
===
    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
===
"""

import time
import multiprocessing as mp

import lib.data_mds as mds
import lib.callback as callback


class PBP:
    def __init__(self):
        self.WebCapture = None

    @staticmethod
    def getTime(time_format="%b %d %Y %H:%M:%S %Z"):
        Time = time.localtime(time.time())
        return time.strftime(time_format, Time)

    def start(self):
        mp.Process(target=mds.listen, args=(0,)).start()
        mp.Process(target=callback.listen, args=(0,)).start()


if __name__ == "__main__":
    handle = PBP()
    print("PBP Server\n{}\n".format(handle.getTime()))
    handle.start()
