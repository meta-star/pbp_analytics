import os
import subprocess

import cv2
import skimage.measure as measure

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
    To render web page from QT Webkit with python-webkit2png.
    But we plan using Gecko/Servo to replace someday.
    """

    def __init__(self):
        pass


class BrowserAgent:
    """
    As a backup solution
    The class will allow you to use your browser as the agent to take a screenshot form it.
    """

    def __init__(self, config):
        using = config.get("capture_browser")
        if using == "firefox":
            self.exec_path = "/usr/bin/firefox"
            self.capture_args = "--screenshot {path} {url} --window-size={size}"
        elif using == "chrome":
            self.exec_path = "/usr/bin/google-chrome"
            self.capture_args = "--headless --screenshot={path} {url} --window-size={size} --hide-scrollbars"
        elif using == "chromium":
            self.exec_path = "/usr/bin/chromium-browser"
            self.capture_args = "--headless --screenshot={path} {url} --window-size={size}"
        else:
            browser_exec_path = config.get("exec_path")
            browser_capture_args = config.get("capture_args")
            assert using is None and browser_exec_path and browser_capture_args, "BrowserAgent Configure Error"
            self.exec_path = config.get("exec_path")
            self.capture_args = config.get("capture_args")

    def set_path(self, path):
        """
        To setup your browser path in your computer.
        :param path: Your browser path.
        :return: bool
        """
        if os.path.exists(path):
            self.exec_path = path
            return True
        else:
            return False

    def capture(self, url, path, size="1920,1080"):
        capture_args = self.capture_args.format(**{"url": url, "path": path, "size": size})
        return subprocess.run([self.exec_path, capture_args], shell=True, check=True)


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
        layout_path = self.cache_path + output_image
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
