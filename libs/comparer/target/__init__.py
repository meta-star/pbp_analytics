from .page_view import View, ViewSample
from ...thread_control import ThreadControl

"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


class Target:
    def __init__(self, pbp_handle):
        self.analytics_tasks = [
            View()
        ]

        self.generate_tasks = [
            ViewSample(pbp_handle)
        ]

    @staticmethod
    def _get_result():
        return 1

    def generate_action(self, url):
        thread_control = ThreadControl()
        for task in self.generate_tasks:
            thread_control.add(
                task.generate,
                ()
            )
        while len(thread_control.multiprocess_list):
            pass
        return self._get_result()

    def analytics_action(self, url):
        thread_control = ThreadControl()
        for task in self.analytics_tasks:
            thread_control.add(
                task.analytics,
                (url,)
            )
        while len(thread_control.multiprocess_list):
            pass
        return self._get_result()
