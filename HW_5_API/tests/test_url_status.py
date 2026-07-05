import pytest
import requests

def pytest_addoption(parser):
    parser.addoption(
        '--url',
        action='store',
        default='https://ya.ru',
        help='URL, который быдет проверяться',
    )

@pytest.fixture
def url_and_status(request):
    return (
        request.config.detoption('--url'),
        request.config.detoption('--status_code'),
    )


def test_url_returns_expected_status(url_and_status):
    url, expected = url_and_status
    resp = requests.get(url, timeout=10)
    assert resp.status_code == expected, (
        f'Для {url} ожидался статус {expected}, но получен {resp.status_code}'
    )