import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


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
def browser(request):
    browser_name = request.config.getoption("--browser").lower()
    base_url = request.config.getoption("--base-url")
    headless = request.config.getoption("--headless")

    driver = None
    try:
        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

        elif browser_name == "firefox":
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument("-headless")
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)

        elif browser_name == "edge":
            options = webdriver.EdgeOptions()
            if headless:
                options.add_argument("--headless=new")
            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=options)
        else:
            pytest.exit(f"Unsupported browser: {browser_name}. Use: chrome, firefox, edge")

        driver.base_url = base_url
        yield driver

    except Exception as e:
        pytest.fail(f"Failed to initialize {browser_name} driver: {e}")
    finally:
        if driver is not None:
            driver.quit()
