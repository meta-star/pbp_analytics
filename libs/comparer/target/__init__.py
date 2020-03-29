from .page_view import View

"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


class Target:
    def __init__(self, pbp_handle):
        self.view_handle = View(pbp_handle)

    def close(self):
        self.view_handle.close()

    async def generate(self):
        """

        :return:
        """
        await self.view_handle.generate()

    def analytics(self, data, url_normalized):
        """

        :param data:
        :param url_normalized:
        :return:
        """
        if "type" in data:
            target_type = data.get("type")
        else:
            target_type = 0

        return self.view_handle.analytics(target_type, url_normalized)
