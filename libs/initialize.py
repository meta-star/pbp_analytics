import asyncio

"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


class Initialize:
    def __init__(self, pbp_handle):
        self.handle = pbp_handle
        self.__config_checker()

    def __config_checker(self):
        return self.__mysql_checker()

    def __mysql_checker(self):
        return self.__env_setup()

    def __mysql_checker_initialize(self):
        pass

    def __mysql_checker_repair(self):
        pass

    def __env_setup(self):
        asyncio.run(self.handle.gen_sample())
