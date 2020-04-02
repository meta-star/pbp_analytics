#!/usr/bin/env python3
"""
Phishing Blocker Project - Analytics

(c)2019 SuperSonic(https://randychen.tk).
===
    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
===
"""

from libs import Analytics, Tools

if __name__ == "__main__":
    handle = Analytics()
    print("PBP Server\n{}\n".format(Tools.get_time()))
    handle.test()
