#!/usr/bin/env python3
"""
Phishing Blocker Project - Analytics (2026 Redesign)

(c)2020-2026 Star Inc.(https://starinc.xyz).
===
    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
===
"""

import uvicorn
import os
from app.config import settings

if __name__ == "__main__":
    # Ensure config loading or env setup if needed
    print(f"Starting PBP Analytics on port {settings.PORT}...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=False)
