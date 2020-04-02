import asyncio
import multiprocessing

from .tools import Tools
from .analytics import Analytics

"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


class Initialize:
    print("""
    Phishing Blocker Project - Analytics
    
    (c)2019 SuperSonic(https://randychen.tk).
    
    Now: {}
    ===
        This Source Code Form is subject to the terms of the Mozilla Public
        License, v. 2.0. If a copy of the MPL was not distributed with this
        file, You can obtain one at http://mozilla.org/MPL/2.0/.
    ===
    """.format(Tools.get_time()))

    def __init__(self, pbp_handle: Analytics):
        self.handle = pbp_handle
        self.__config_checker()

    def __config_checker(self):
        return self.__mysql_checker()

    def __mysql_checker(self):
        pass

    def __mysql_checker_initialize(self):
        pass

    def __mysql_checker_repair(self):
        pass

    @staticmethod
    def env_setup(pbp_handle):
        threads = EnvironmentClean(pbp_handle)
        threads.start()
        threads.join()


class EnvironmentClean(multiprocessing.Process):
    def __init__(self, pbp_handle):
        multiprocessing.Process.__init__(self)
        self.handle = pbp_handle

    def run(self):
        asyncio.run(self.handle.gen_sample())
