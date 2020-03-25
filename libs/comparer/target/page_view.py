from hashlib import sha256
from threading import Thread

from .page_view_tools import WebCapture

"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


class View:
    def __init__(self, pbp_handle):
        self.handle = WebCapture(pbp_handle.cfg["WebCapture"])
        self.data_control = pbp_handle.data_control

    def _capture(self, url):
        url_hash = sha256(url.encode("utf-8"))
        layout_path = self.handle.get_page_image(
            target_url=url,
            output_image="{}.png".format(
                url_hash.hexdigest()
            )
        )
        image_num_array = self.handle.image_object(layout_path)
        dump_num_array = image_num_array.dumps()
        hash_object = sha256(image_num_array)
        return hash_object.hexdigest(), dump_num_array

    def _signature(self, hex_digest):
        query = self.data_control.find_page_by_view_signature(hex_digest)
        if query:
            return query[0]

    def _render(self, target_num_array):
        trust_samples = self.data_control.get_view_narray_from_trustlist()
        for sample in trust_samples:
            origin_sample = self.handle.image_object_from_string(
                sample["target_view_narray"].encode("utf-8")
            )
            yield sample["url"], self.handle.image_compare(
                target_num_array,
                origin_sample
            )

    def analytics(self, target_url):
        (view_signature, view_data) = self._capture(target_url)

        signature_query = self._signature(view_signature)
        if signature_query:
            return list(signature_query)

        query = {url: score for url, score in self._render(view_data)}
        return [url for url in query if query[url] > 0.5 and query[url] == max(query.values())]

    def generate(self):
        for origin_url in self.data_control.get_urls_from_trustlist():
            (view_signature, view_data) = self._capture(origin_url)
            thread = Thread(
                target=self.data_control.upload_view_sample,
                args=(
                    origin_url,
                    view_signature,
                    view_data,
                )
            )
            thread.start()
            thread.join()
