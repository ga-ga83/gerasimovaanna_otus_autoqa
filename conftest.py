import pytest
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import WebDriverException
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
logger = logging.getLogger(__name__)


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
    url = request.config.getoption("--base-url").rstrip("/") + "/"
    logger.info(f"Base URL for tests: {url}")
    return url


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

            options.set_capability("browserName", browser_name)
            if browser_version:
                options.set_capability("browserVersion", browser_version)
            options.set_capability("selenoid:options", {
                "enableVNC": True,
                "enableVideo": False,
                "enableLog": True,
            })

            logger.info(f"Connecting to Selenoid at {selenoid_url} with {browser_name} v{browser_version or 'latest'}")
            driver = webdriver.Remote(
                command_executor=selenoid_url,
                options=options,
            )

        # ── Локальный режим ──
        else:
            logger.info(f"Starting local {browser_name} browser in {'headless' if headless else 'normal'} mode")
            if browser_name == "chrome":
                options = ChromeOptions()
                if headless:
                    options.add_argument("--headless=new")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                # Для отладки в Docker иногда полезно добавить:
                # options.add_argument("--remote-debugging-port=9222")
                driver = webdriver.Chrome(options=options)

            elif browser_name == "firefox":
                options = FirefoxOptions()
                if headless:
                    options.add_argument("--headless")
                driver = webdriver.Firefox(options=options)

            else:
                pytest.fail(f"Unsupported browser: {browser_name}. Use: chrome, firefox")

        driver.base_url = base_url

        # ВАЖНО: ждём полной загрузки страницы после старта браузера.
        # Это критично для PrestaShop Admin, иначе первые тесты будут падать на TimeoutException.
        driver.get(base_url)
        logger.info("Waiting for document ready state...")
        driver.execute_script("return document.readyState")  # просто чтобы инициировать сессию
        # Selenium сам ждёт загрузки при get(), но для тяжёлых SPA/админок можно добавить явное ожидание:
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait

        # Пытаемся дождаться хотя бы наличия body — это признак того, что страница начала рендериться
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        logger.info("Browser initialized and page started loading successfully.")

    except WebDriverException as e:
        pytest.fail(f"Failed to initialize {browser_name} driver: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error while initializing browser: {e}")

    yield driver

    if driver is not None:
        try:
            driver.quit()
        except Exception as e:
            logger.warning(f"Error while closing driver: {e}")


@pytest.fixture
def pages(browser, base_url):
    logger_page = logging.getLogger("PageObjects")
    return {
        "home": HomePage(browser, base_url, logger_page),
        "catalog": CatalogPage(browser, base_url, logger_page),
        "product": ProductPage(browser, base_url, logger_page),
        "login": LoginPage(browser, base_url, logger_page),
        "registration": RegistrationPage(browser, base_url, logger_page),
        "administration": AdminPage(browser, base_url, logger_page)
    }


@pytest.fixture()
def logger():
    return logging.getLogger(__name__)


# Хук для прикрепления скриншотов к отчётам Allure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # Если тест упал на этапе выполнения (call)
    if rep.when == "call" and rep.failed:
        # Пытаемся получить доступ к драйверу через фикстуру 'pages', если она была создана
        try:
            # Получаем pages только если они есть в кэше фикстур текущего теста
            # Это безопаснее, чем пытаться вызвать getfixturevalue в teardown
            pages_fixture = item.funcargs.get("pages")

            if pages_fixture:
                # Берём драйвер из любого page-объекта (они все используют один driver)
                driver = next(iter(pages_fixture.values())).driver

                if driver:
                    screenshot = driver.get_screenshot_as_png()
                    allure.attach(
                        screenshot,
                        name=f'Screenshot_on_failure_{item.name}',
                        attachment_type=allure.attachment_type.PNG
                    )
                    logger.info(f"Screenshot attached for failed test: {item.name}")
                else:
                    logger.warning("Could not take screenshot: driver is None")
            else:
                logger.warning("Could not take screenshot: 'pages' fixture was not available")
        except Exception as e:
            logger.error(f"Error attaching screenshot: {e}")
