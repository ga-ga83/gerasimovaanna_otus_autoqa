import pytest
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import allure

from HW_8.pages.admin_page import AdminPage
from HW_8.pages.home_page import HomePage
from HW_8.pages.catalog_page import CatalogPage
from HW_8.pages.product_page import ProductPage
from HW_8.pages.login_page import LoginPage
from HW_8.pages.registration_page import RegistrationPage

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
_log = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", choices=["chrome", "firefox"], help="Browser to run tests with")
    parser.addoption("--base-url", action="store", default="http://prestashop:80", help="Base URL for tests")
    parser.addoption("--headless", action="store_true", default=True, help="Run browser in headless mode")
    parser.addoption("--selenoid-url", action="store", default=None, help="Selenoid URL")
    parser.addoption("--browser-version", action="store", default="", help="Browser version for Selenoid")


@pytest.fixture(scope="session")
def base_url(request) -> str:
    url = request.config.getoption("--base-url").rstrip("/") + "/"
    _log.info(f"Base URL for tests: {url}")
    return url


@pytest.fixture(scope="session")
def browser(request, base_url):
    browser_name = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")
    selenoid_url = request.config.getoption("--selenoid-url")
    browser_version = request.config.getoption("--browser-version")

    driver = None

    try:
        if selenoid_url:
            if browser_name == "chrome":
                options = ChromeOptions()
            elif browser_name == "firefox":
                options = FirefoxOptions()
            else:
                pytest.exit(f"Unsupported browser: {browser_name}")

            options.set_capability("browserName", browser_name)
            if browser_version:
                options.set_capability("browserVersion", browser_version)
            options.set_capability("selenoid:options", {
                "enableVNC": True,
                "enableVideo": False,
                "enableLog": True,
            })
            _log.info(f"Connecting to Selenoid: {selenoid_url}")
            driver = webdriver.Remote(command_executor=selenoid_url, options=options)
        else:
            _log.info(f"Starting local {browser_name} (headless={headless})")
            if browser_name == "chrome":
                options = ChromeOptions()
