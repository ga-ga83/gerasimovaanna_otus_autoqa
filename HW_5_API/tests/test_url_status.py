import pytest
import requests


@pytest.fixture
def url_and_status(request):
    # имена без дефисов: это то, что попадает в config.option
    url = request.config.getoption("url")
    expected_status = request.config.getoption("status_code")
    return url, expected_status


def test_url_returns_expected_status(url_and_status):
    url, expected = url_and_status
    resp = requests.get(url, timeout=10)
    assert resp.status_code == expected, (
        f"Для {url} ожидался статус {expected}, но получен {resp.status_code}"
    )

