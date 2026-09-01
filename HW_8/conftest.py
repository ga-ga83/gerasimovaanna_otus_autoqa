import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
import allure

from HW_8.pages.admin_page import AdminPage
#from webdriver_manager.chrome import ChromeDriverManager
#from webdriver_manager.firefox import GeckoDriverManager
#from webdriver_manager.microsoft import EdgeChromiumDriverManager

from HW_8.pages.home_page import HomePage
from HW_8.pages.catalog_page import CatalogPage
from HW_8.pages.product_page import ProductPage
from HW_8.pages.login_page import LoginPage
from HW_8.pages.registration_page import RegistrationPage
from HW_8.pages.base_page import BasePage


#Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

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
    #Передаем логгер в страницы для удобства
    logger = logging.getLogger("PageObjects")
    return {
        "home": HomePage(browser, base_url,logger),
        "catalog": CatalogPage(browser, base_url, logger),
        "product": ProductPage(browser, base_url, logger),
        "login": LoginPage(browser, base_url, logger),
        "registration": RegistrationPage(browser, base_url, logger),
        "administration": AdminPage(browser, base_url, logger)
    }

#фикстура длЯ логгера
@pytest.fixture()
def logger():
    return logging.getLogger(__name__)

#фикстура для скриншота при падении теста
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Сохраняет результат выполнения теста в атрибут узла, чтобы фикстуры могли его прочитать."""
    outcome = yield
    rep = outcome.get_result()

    # Сохраняем только результат этапа 'call' (сам запуск теста)
    if rep.when == "call":
        setattr(item, "rep_call", rep)


@pytest.fixture(autouse=True)
def take_screenshot_on_failure(request):
    """Автоматически делает скриншот при падении любого теста"""
    yield  # Здесь выполняется сам тест

    # Проверяем, что атрибут существует и тест упал
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        try:
            # Получаем pages через getfixturevalue — это безопасно даже если фикстура уже завершилась
            pages = request.getfixturevalue("pages")
            driver = pages["home"].driver

            # Делаем скриншот
            screenshot = driver.get_screenshot_as_png()

            allure.attach(
                screenshot,
                name=f'Screenshot_on_failure_{request.node.name}',
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            # Если не удалось сделать скриншот (например, браузер закрыт), просто логируем ошибку,
            # чтобы не ломать отчёт по этой причине
            print(f"Не удалось сделать скриншот для теста {request.node.name}: {e}")