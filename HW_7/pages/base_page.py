from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:
    def __init__(self, driver: WebDriver, base_url: str):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, timeout=10)

    def open(self, url=None):
        if url:
            self.driver.get(url)
        else:
            self.driver.get(self.base_url)
    #helper methods for waiting
    def wait_for_element(self, locator, timeout=10):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator, timeout=10):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_for_presence(self, locator, timeout=10):
        return self.wait.until(EC.presence_of_element_located(locator))

    def get_title(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url
