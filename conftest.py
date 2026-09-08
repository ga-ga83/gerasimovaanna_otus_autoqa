import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
# Edge пока убираем из импортов, так как браузера нет в образе
# from selenium.webdriver.edge.service import Service as EdgeService
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
        # Убрали 'edge', так как его нет в текущем Docker образе
        choices=["chrome", "firefox"],
        help="Browser to run tests with: chrome, firefox"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="http://host.docker.internal:8081/", # Важно для Docker! localhost внутри контейнера - это сам контейнер
        help="Base URL for tests"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=True, # В Docker всегда лучше запускать headless
        help="Run browser in headless mode"
    )

@pytest.fixture(scope="session")
def base_url(request) -> str:
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

            # !!! КРИТИЧЕСКИ ВАЖНО ДЛЯ DOCKER !!!
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            # Отключаем предупреждения в логах
            options.add_argument("--disable-gpu")

            driver = webdriver.Chrome(options=options)

        elif browser_name == "firefox":
            options = webdriver.FirefoxOptions()
            if headless:
                # ИСПРАВЛЕНО: было "-headless", стало "--headless"
                options.add_argument("--headless")

            driver = webdriver.Firefox(options=options)

        # Блок для Edge удален, так как браузера нет в образе.
        # Если очень нужен Edge, придется ставить его в Dockerfile аналогично Chrome.
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

    # Проверка: упал ли тест?
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        try:
            # Пытаемся получить страницы, но оборачиваем в try-except,
            # если фикстура pages не успела инициализироваться
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
