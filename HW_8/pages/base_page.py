import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import allure


class BasePage:
    def __init__(self, driver: WebDriver, base_url: str, logger: logging.Logger = None):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, timeout=10)
        self.logger = logger or logging.getLogger(self.__class__.__name__)

    def open(self, url=None):
        with allure.step(f"Открытие страницы: {url or self.base_url}"):
            self.logger.info(f"Открытие страницы: {url or self.base_url}")
            if url:
                self.driver.get(url)
            else:
                self.driver.get(self.base_url)

    # helper methods for waiting
    def wait_for_element(self, locator, timeout=10):
        with allure.step(f"Ожидание элемента (видимость): {locator}"):
            self.logger.debug(f"Ожидание элемента: {locator}")
            return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator, timeout=10):
        with allure.step(f"Ожидание кликабельности: {locator}"):
            self.logger.debug(f"Ожидание кликабельности: {locator}")
            return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_for_presence(self, locator, timeout=10):
        with allure.step(f"Ожидание появления в DOM: {locator}"):
            self.logger.debug(f"Ожидание появления в DOM: {locator}")
            return self.wait.until(EC.presence_of_element_located(locator))

    def get_title(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url

    # Хелпер для клика с логированием
    def click_element(self, locator):
        el = self.wait_for_clickable(locator)
        with allure.step(f"Клик по элементу: {locator}"):
            self.logger.info(f"Клик по элементу: {locator}")
            el.click()
