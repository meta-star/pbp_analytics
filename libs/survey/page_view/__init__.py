import asyncio
import base64
from threading import Thread, Lock

from .image import Image

"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


class View:
    def __init__(self, pbp_handle):
        self.data_control = pbp_handle.data_control
        self.image_handle = Image(pbp_handle)

    def close(self):
        """

        :return:
        """
        self.image_handle.capture_handle.browser.close()

    async def analytics(self, target_type, target_url):
        """

        :param target_type:
        :param target_url:
        :return:
        """
        (view_signature, view_data) = await self.image_handle.capture(target_url)

        signature_query = await self.image_handle.signature(view_signature)
        yield signature_query

        if signature_query:
            return

        query = {}
        async for url, score in self.image_handle.rank(target_type, view_data):
            query[url] = score

        for url in query:
            if query[url] > 0.95 and query[url] == max(query.values()):
                yield url

    async def generate(self):
        """

        :return:
        """
        thread = None
        lock = Lock()

        async def _upload(url):
            lock.acquire()
            (view_signature, view_data) = await self.image_handle.capture(url)
            b64_view_data = base64.b64encode(view_data.dumps())
            self.data_control.upload_view_sample(
                url,
                view_signature,
                b64_view_data,
            )
            lock.release()

        for origin_url in self.data_control.get_urls_from_trustlist():
            thread = Thread(
                target=lambda url: asyncio.run(_upload(url)),
                args=(
                    origin_url,
                )
            )
            thread.start()

        if thread:
            thread.join()
