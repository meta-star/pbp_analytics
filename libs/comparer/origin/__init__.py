"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


class Origin:
    def __init__(self, pbp_handle):
        self.pbp_handle = pbp_handle

    def generate(self):
        pass

    def action(self, origin_url, target_url):
        return 1
