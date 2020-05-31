#!/usr/bin/env python3
"""
Phishing Blocker Project - Analytics

(c)2020 Star Inc.(https://starinc.xyz).
===
    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
===
"""

from libs import Analytics
import os

if __name__ == "__main__":
    config_type = "ENV" if "PBP_CFG" in os.environ else "config.ini"
    handle = Analytics(config_type)
    handle.start()
