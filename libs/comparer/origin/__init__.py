from .domain_resolve import DomainResolve
from ...thread_control import ThreadControl

"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


class Origin:
    def __init__(self, pbp_handle):
        self.pbp_handle = pbp_handle
        self.tasks = [
            DomainResolve()
        ]

    @staticmethod
    def _get_result():
        return 1

    def action(self, url):
        thread_control = ThreadControl()
        for task in self.tasks:
            thread_control.add(
                task.analytics,
                (url,)
            )
        while len(thread_control.multiprocess_list):
            pass
        return self._get_result()
