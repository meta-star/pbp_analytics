from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from app.config import settings
import logging

class BrowserService:
    def __init__(self):
        self.browser_type = settings.CAPTURE_BROWSER

    def _get_driver(self):
        if self.browser_type == "firefox":
            options = FirefoxOptions()
            options.add_argument("--headless")
            # options.add_argument("--private-window") # Firefox might not need explicit private window in headless
            return webdriver.Firefox(options=options)
        elif self.browser_type == "chrome":
            options = ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--incognito")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            return webdriver.Chrome(options=options)
        else:
            raise ValueError(f"Unsupported browser type: {self.browser_type}")

    def capture_screenshot(self, url: str, output_path: str, width: int = 1920, height: int = 1080):
        driver = None
        try:
            driver = self._get_driver()
            driver.set_window_size(width, height)
            driver.set_page_load_timeout(30)
            driver.get(url)
            driver.save_screenshot(output_path)
        except Exception as e:
            logging.error(f"Error capturing screenshot for {url}: {e}")
            raise e
        finally:
            if driver:
                driver.quit()

browser_service = BrowserService()
