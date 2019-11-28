import os
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
    """
    def __init__(self):
        pass


class BrowserAgent:
    """
        As a backup solution
        The class will allow you to use your browser as the agent to take a screen shot form it.
    """
    def __init__(self, using):
        if using == "firefox":
            self.exec_path = "/usr/bin/firefox"
            self.capture_com = "--screenshot {path} {url} --window-size={size}"
        elif using == "chrome":
            self.exec_path = "/usr/bin/google-chrome"
            self.capture_com = "--headless --screenshot={path} {url} --window-size={size} --hide-scrollbars"
        elif using == "chromium":
            self.exec_path = "/usr/bin/chromium-browser"
            self.capture_com = "--headless --screenshot={path} {url} --window-size={size}"
        else:
            assert using is dict, "Configure Error"
            self.exec_path = using["exec_path"]
            self.capture_com = using["capture_com"]

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
        capture_com = self.capture_com.format(**{"url": url, "path": path, "size": size})
        return os.system("{} {}".format(self.exec_path, capture_com))

# Capture


class WebCapture:
    """
        To take screen shot for PBP.
    """
    def __init__(self, browser_agent, cache_path="./temp/", compare_path="./web_archive/"):
        self.cache_path = cache_path
        self.compare_path = compare_path

        self.browser = browser_agent

        if not os.path.exists(self.cache_path):
            os.mkdir(self.cache_path)
        if not os.path.exists(self.compare_path):
            os.mkdir(self.compare_path)

    def get_page_image(self, target_url, output_image='out.png', agent="PC"):
        """
            To get the image of the URL you provided.
            :param target_url: The target URL
            :param output_image: Output path (optional)
            :param agent: PC or Mobile as user-agent, it will not work if you are using BrowserAgent (optional)
            :return: bool
        """
        if os.path.isfile(self.cache_path + output_image):
            os.remove(self.cache_path + output_image)
        self.browser.capture(target_url, self.cache_path + output_image)
        return True

    @staticmethod
    def image_compare(img1, img2):
        """
            To compare image using structural similarity index
            :param img1: Image object
            :param img2: Image object
            :return: float of the similar lever
        """
        return measure.compare_ssim(img1, img2, multichannel=True)


class WebSourceCompare:
    def get(self):
        pass

    def compare(self):
        pass
