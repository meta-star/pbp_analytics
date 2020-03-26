from .page_view import View

"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


class Target:
    def __init__(self, pbp_handle):
        self.tasks = [
            View(pbp_handle)
        ]

    def generate(self):
        for task in self.tasks:
            task.generate()

    def analytics(self, url):
        for task in self.tasks:
            yield task.analytics(url)
