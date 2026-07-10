import json
import os
import requests
from HW_5_API.helpers.logger import logger


class BaseService:
    @staticmethod
    def _default_headers():
        return {
            "accept": "application/json",
            "User-Agent": "MyTestAgent/1.0 (OTUS HW-5)"
        }

    @staticmethod
    def _get_proxies():
        # Автоматически берем из переменных окружения, если они заданы
        http_proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
        https_proxy = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")

        if http_proxy or https_proxy:
            return {
                "http": http_proxy,
                "https": https_proxy or http_proxy
            }
        return None

    def get(self, url, params=None, headers=None, code=None, timeout=10):
        final_headers = self._default_headers()
        if headers:
            final_headers.update(headers)

        proxies = self._get_proxies()  # Получаем прокси или None

        try:
            # Если proxies=None, requests просто игнорирует этот аргумент
            response = requests.get(
                url,
                params=params,
                headers=final_headers,
                timeout=timeout,
                proxies=proxies
            )

            if code is None:
                response.raise_for_status()
            else:
                assert response.status_code == code, f"Expected {code}, got {response.status_code}"

            logger.info("OK. URL: %s, Code: %d", url, response.status_code)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error("Error. URL: %s, Error: %s", url, str(e))
            return None

    def delete(self, url, headers):
        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            logger.info("OK. URL: %s, Code: %d", url, response.status_code)
            if not response.text:
                return {}  # или None, в зависимости от того, что ждут тесты
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error("Error. %s", str(e))
            return None

    def post(self, url, body):
        try:
            headers = {'accept': "application/json", 'Content-Type': 'application/json'}
            response = requests.post(url, data=json.dumps(body), headers=headers)
            response.raise_for_status()
            logger.info("OK. URL: %s, Code: %d", url, response.status_code)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error("Error. %s", str(e))
            return None

    def put(self, url, body, headers):
        try:
            response = requests.put(url, data=json.dumps(body), headers=headers)
            response.raise_for_status()
            logger.info("OK. URL: %s, Code: %d", url, response.status_code)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error("Error. %s", str(e))
            return None

