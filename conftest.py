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
    parser.addoption("--browser", action="store", default="chrome", choices=["chrome", "firefox"],
                     help="Browser to run tests with")
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
                if headless:
                    options.add_argument("--headless=new")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                # Важно для стабильности в Docker
                options.add_argument("--window-size=1920,1080")
                driver = webdriver.Chrome(options=options)

            elif browser_name == "firefox":
                options = FirefoxOptions()
                if headless:
                    options.add_argument("--headless")
                driver = webdriver.Firefox(options=options)
            else:
                pytest.fail(f"Unsupported browser: {browser_name}")

        driver.base_url = base_url

        # --- ИСПРАВЛЕНИЕ 1: Скрываем панель Symfony ---
        # Это нужно сделать ДО первого перехода на страницу админки,
        # но так как мы не знаем, куда пойдем первым, делаем это сразу после создания драйвера.
        # Cookie 'symfony/web_profiler' со значением '0' скрывает тулбар.
        try:
            # Просто создаем сессию, чтобы можно было ставить куки
            driver.get("about:blank")
            driver.add_cookie({'name': 'symfony/web_profiler', 'value': '0', 'path': '/'})
            _log.info("Symfony Web Debug Toolbar disabled via cookie.")
        except Exception as e:
            _log.warning(f"Could not set cookie to hide Symfony toolbar: {e}")

        # --- ИСПРАВЛЕНИЕ 2: Ждем полной загрузки страницы при старте ---
        _log.info("Navigating to base URL and waiting for stability...")
        driver.get(base_url)

        # Ждем появления body, но даем больше времени для тяжелой админки
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Небольшая пауза, чтобы скрипты админки точно отработали (PrestaShop очень тяжелый JS)
        import time
        time.sleep(2)
        _log.info("Browser initialized successfully.")

    except WebDriverException as e:
        pytest.fail(f"Failed to initialize driver: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")

    yield driver

    if driver is not None:
        try:
            driver.quit()
        except Exception as e:
            _log.warning(f"Error closing driver: {e}")


@pytest.fixture
def pages(browser, base_url):
    page_logger = logging.getLogger("PageObjects")
    return {
        "home": HomePage(browser, base_url, page_logger),
        "catalog": CatalogPage(browser, base_url, page_logger),
        "product": ProductPage(browser, base_url, page_logger),
        "login": LoginPage(browser, base_url, page_logger),
        "registration": RegistrationPage(browser, base_url, page_logger),
        "administration": AdminPage(browser, base_url, page_logger)
    }


@pytest.fixture()
def logger():
    return logging.getLogger(__name__)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            pages_fixture = item.funcargs.get("pages")
            if pages_fixture:
                driver = next(iter(pages_fixture.values())).driver
                if driver:
                    screenshot = driver.get_screenshot_as_png()
                    allure.attach(
                        screenshot,
                        name=f'Screenshot_on_failure_{item.name}',
                        attachment_type=allure.attachment_type.PNG
                    )
                    _log.info(f"Screenshot attached for failed test: {item.name}")
        except Exception as e:
            _log.error(f"Error attaching screenshot: {e}")
