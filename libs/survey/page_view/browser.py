import os
import time

from blink2png_bridge import Blink2pngBridge
from selenium import webdriver

"""
    Copyright (c) 2020 Star Inc.(https://starinc.xyz)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


# Browser Simulation

class BrowserRender:
    """
    The main solution
    To render web page from QTWebEngine with blink2png.
    But we plan using Gecko/Servo to replace someday.
    """

    driver = None

    def __init__(self, capture_browser: str):
        self.using = capture_browser  # Not used
        self.driver = Blink2pngBridge()

    def capture(self, url: str, path: str, size: str = "1920,1080"):
        assert self.driver, "Web Driver Not Existed."
        (width, height) = size.split(",")
        self.driver.set_window_size(width, height)
        self.driver.set_wait(1)
        self.driver.set_timeout(3)
        self.driver.save_screenshot(url, path)

    def close(self):
        pass


class BrowserAgent:
    """
    As a backup solution
    To capture web page via Selenium with webdriver.
    The class will allow you to use your browser as the agent to take a screenshot form it.
    """

    driver = None

    def __init__(self, capture_browser: str):
        self.using = capture_browser
        self.driver = self._set_browser()

    def _set_browser(self):
        if self.using == "firefox":
            options = webdriver.FirefoxOptions()
            options.add_argument('--headless')
            options.add_argument('--private-window')
            return webdriver.Firefox(firefox_options=options)
        elif self.using == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--incognito')
            options.add_argument('--disable-gpu')
            return webdriver.Chrome(chrome_options=options)
        raise BrowserException("BrowserAgent", "No Supported Browser Selected")

    def capture(self, url: str, path: str, size: str = "1920,1080"):
        assert self.driver, "Web Driver Not Existed."
        (width, height) = size.split(",")
        self.driver.set_window_size(width, height)
        self.driver.get(url)
        self.driver.save_screenshot(path)

    def close(self):
        self.driver.close()


class BrowserException(Exception):
    def __init__(self, cause, message):
        self.cause = cause
        self.message = message

    def __str__(self):
        return self.cause + ': ' + self.message
