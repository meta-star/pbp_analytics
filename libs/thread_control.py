import multiprocessing

"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


class ThreadControl:
    multiprocess_list = {}

    def add(self, function, args=()):
        added_multiprocess = multiprocessing.Process(name=function.__name__, target=function, args=args)
        self.multiprocess_list[function.__name__] = added_multiprocess
        added_multiprocess.start()

    def stop(self, function_name):
        assert function_name in self.multiprocess_list
        self.multiprocess_list[function_name].terminate()
