from hashlib import sha256

from .page_view_tools import WebCapture

"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


class ViewSample:
    def __init__(self, pbp_handle):
        self.handle = WebCapture(pbp_handle.cfg["WebCapture"])
        self.data_control = pbp_handle.data_control

    def _capture(self, url):
        url_hash = sha256(url.encode("utf-8"))
        layout_path = self.handle.get_page_image(
            url,
            "{}.png".format(
                url_hash.hexdigest()
            )
        )
        image_num_array = self.handle.image_object(layout_path)
        hash_object = sha256(image_num_array)
        return hash_object.hexdigest()

    def generate(self):
        for url in self.data_control.get_urls_from_trustlist():
            self.data_control.upload_view_sample(
                url=url,
                view_signature=self._capture(url)
            )


class View:
    def _signature(self):
        pass

    def _render(self):
        pass

    def analytics(self, url):
        pass
