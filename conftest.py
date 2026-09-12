import pytest
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import allure

from HW_8.pages.admin_page import AdminPage
from HW_8.pages.home_page import HomePage
from HW_8.pages.catalog_page import CatalogPage
from HW_8.pages.product_page import ProductPage
from HW_8.pages.login_page import LoginPage
from HW_8.pages.registration_page import RegistrationPage
from HW_8.pages.base_page import BasePage

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox"],
        help="Browser to run tests with: chrome, firefox"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="http://prestashop:80",
        help="Base URL for tests"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=True,
        help="Run browser in headless mode"
    )
    parser.addoption(
        "--selenoid-url",
        action="store",
        default=None,
        help="Selenoid URL (e.g. http://selenoid:4444/wd/hub). If not set, runs locally."
    )
    parser.addoption(
        "--browser-version",
        action="store",
        default="",
        help="Browser version for Selenoid (e.g. 128.0)"
    )


@pytest.fixture(scope="session")
def base_url(request) -> str:
    return request.config.getoption("--base-url").rstrip("/") + "/"


@pytest.fixture(scope="session")
def browser(request, base_url):
    browser_name = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")
    selenoid_url = request.config.getoption("--selenoid-url")
    browser_version = request.config.getoption("--browser-version")

    driver = None
    try:
        # ── Режим Selenoid (Remote WebDriver) ──
        if selenoid_url:
            if browser_name == "chrome":
                options = ChromeOptions()
            elif browser_name == "firefox":
                options = FirefoxOptions()
            else:
                pytest.exit(f"Unsupported browser: {browser_name}")

            # Передаём capability для Selenoid: VNC, видео, логи
            options.set_capability("browserName", browser_name)
            if browser_version:
                options.set_capability("browserVersion", browser_version)
            options.set_capability("selenoid:options", {
                "enableVNC": True,
                "enableVideo": False,
                "enableLog": True,
            })

            driver = webdriver.Remote(
                command_executor=selenoid_url,
                options=options,
            )

        # ── Локальный режим (как раньше) ──
        else:
            if browser_name == "chrome":
                options = ChromeOptions()
                if headless:
                    options.add_argument("--headless=new")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                driver = webdriver.Chrome(options=options)

            elif browser_name == "firefox":
                options = FirefoxOptions()
                if headless:
                    options.add_argument("--headless")
                driver = webdriver.Firefox(options=options)

            else:
                pytest.exit(f"Unsupported browser: {browser_name}. Use: chrome, firefox")

        driver.base_url = base_url
        yield driver

    except Exception as e:
        pytest.fail(f"Failed to initialize {browser_name} driver: {e}")
    finally:
        if driver is not None:
            driver.quit()


@pytest.fixture
def pages(browser, base_url):
    logger = logging.getLogger("PageObjects")
    return {
        "home": HomePage(browser, base_url, logger),
        "catalog": CatalogPage(browser, base_url, logger),
        "product": ProductPage(browser, base_url, logger),
        "login": LoginPage(browser, base_url, logger),
        "registration": RegistrationPage(browser, base_url, logger),
        "administration": AdminPage(browser, base_url, logger)
    }


@pytest.fixture()
def logger():
    return logging.getLogger(__name__)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        setattr(item, "rep_call", rep)


@pytest.fixture(autouse=True)
def take_screenshot_on_failure(request):
    yield

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        try:
            pages = request.getfixturevalue("pages")
            driver = pages["home"].driver

            if driver:
                screenshot = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name=f'Screenshot_on_failure_{request.node.name}',
                    attachment_type=allure.attachment_type.PNG
                )
            else:
                print("Не удалось сделать скриншот: драйвер не был создан.")

        except Exception as e:
            print(f"Ошибка при создании скриншота: {e}")
