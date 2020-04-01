from selenium import webdriver

"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

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

    def __init__(self):
        pass


class BrowserAgent:
    """
    As a backup solution
    To capture web page via Selenium with webdriver.
    The class will allow you to use your browser as the agent to take a screenshot form it.
    """

    driver = None

    def __init__(self, config):
        using = config.get("capture_browser")
        if using == "firefox":
            options = webdriver.FirefoxOptions()
            options.add_argument('--headless')
            options.add_argument('--private-window')
            self.driver = webdriver.Firefox(firefox_options=options)
        elif using == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--incognito')
            options.add_argument('--disable-gpu')
            self.driver = webdriver.Chrome(chrome_options=options)

    def capture(self, url, path, size="1920,1080"):
        (width, height) = size.split(",")
        self.driver.set_window_size(width, height)
        self.driver.get(url)
        self.driver.save_screenshot(path)

    def close(self):
        self.driver.close()
