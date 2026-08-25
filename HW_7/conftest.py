import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

from HW_7.pages.admin_page import AdminPage
#from webdriver_manager.chrome import ChromeDriverManager
#from webdriver_manager.firefox import GeckoDriverManager
#from webdriver_manager.microsoft import EdgeChromiumDriverManager

from HW_7.pages.home_page import HomePage
from HW_7.pages.catalog_page import CatalogPage
from HW_7.pages.product_page import ProductPage
from HW_7.pages.login_page import LoginPage
from HW_7.pages.registration_page import RegistrationPage
from HW_7.pages.base_page import BasePage


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox", "edge"],
        help="Browser to run tests with: chrome, firefox, edge"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="http://localhost:8081/",
        help="Base URL for tests"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )


@pytest.fixture(scope="session")
def base_url(request) -> str:
    """Фикстура для получения базового URL."""
    return request.config.getoption("--base-url")


@pytest.fixture(scope="session")
def browser(request, base_url):
    browser_name = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")

    driver = None
    try:
        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            # Менеджер больше не нужен, Selenium всё сделает сам:
            driver = webdriver.Chrome(options=options)

        elif browser_name == "firefox":
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument("-headless")
            # Просто передаем опции:
            driver = webdriver.Firefox(options=options)

        elif browser_name == "edge":
            options = webdriver.EdgeOptions()
            if headless:
                options.add_argument("--headless=new")
            # Просто передаем опции:
            driver = webdriver.Edge(options=options)
        else:
            pytest.exit(f"Unsupported browser: {browser_name}. Use: chrome, firefox, edge")

        driver.base_url = base_url
        yield driver

    except Exception as e:
        pytest.fail(f"Failed to initialize {browser_name} driver: {e}")
    finally:
        if driver is not None:
            driver.quit()


@pytest.fixture
def pages(browser, base_url):
    return {
        "home": HomePage(browser, base_url),
        "catalog": CatalogPage(browser, base_url),
        "product": ProductPage(browser, base_url),
        "login": LoginPage(browser, base_url),
        "registration": RegistrationPage(browser, base_url),
        "administration": AdminPage(browser, base_url)
    }
