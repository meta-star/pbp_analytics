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

import sys
import asyncio

sys.path.append("..")
from libs import Analytics


async def main():
    config = "../config.ini"
    handle = Analytics(config)
    if len(sys.argv) != 2:
        handle.stop()
        sys.exit()
    async for x in handle.view_survey.analyze(0, sys.argv[1]):
        print(x)


if __name__ == "__main__":
    asyncio.run(main())
