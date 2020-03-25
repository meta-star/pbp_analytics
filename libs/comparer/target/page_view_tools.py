import os

import cv2
import skimage.measure as measure
from arsenic import browsers, services, get_session

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
    def __init__(self, config):
        self.browser = config.get("capture_browser")

    def _get_browser(self):
        if self.browser == "firefox":
            service = services.Geckodriver()
            browser = browsers.Firefox(firefoxOptions={
                'args': ['-headless']
            })
        elif self.browser == "chrome":
            service = services.Chromedriver()
            browser = browsers.Chrome(chromeOptions={
                'args': ['--headless', '--disable-gpu']
            })
        return (service, browser)

    async def capture(self, url, path, size="1920,1080"):
        async with get_session(*self._get_browser()) as driver:
            (width, height) = size.split(",")
            driver.set_window_size(width, height)
            driver.get(url)
            await driver.save_screenshot(path)


# Capture

class WebCapture:
    """
    To take screenshot for PBP.
    """

    def __init__(self, config):
        self.cache_path = config["cache_path"]

        self.browser = self.__set_browser_simulation(
            config["capture_type"]
        )(config)

        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)

    @staticmethod
    def __set_browser_simulation(type_id):
        """
        Set Browser Simulation by ID
        :param type_id: Type ID
        :return: class object
        """
        return {
            '1': BrowserRender,
            '2': BrowserAgent
        }[type_id]

    def get_page_image(self, target_url, output_image='out.png'):
        """
        To get the image of the URL you provided.
        :param target_url: The target URL
        :param output_image: Output path (optional)
        :return: bool
        """
        layout_path = os.path.join(self.cache_path, output_image)
        if os.path.isfile(layout_path):
            os.remove(layout_path)
        self.browser.capture(target_url, layout_path)
        return layout_path

    @staticmethod
    def image_object(path):
        """
        Create NumPy Array by OpenCV
        :param path: The Image Path
        :return: Image object
        """
        return cv2.imread(path, 0)

    @staticmethod
    def image_compare(img1, img2):
        """
        To compare image using structural similarity index
        :param img1: Image object
        :param img2: Image object
        :return: float of the similar lever
        """
        return measure.compare_ssim(img1, img2, multichannel=True)
