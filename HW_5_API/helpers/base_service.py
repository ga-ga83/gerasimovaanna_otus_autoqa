import json
import requests
from typing import Any, Dict, Optional, Union

from HW_5_API.helpers.logger import logger

class BaseService():
    '''Универсальный обработчик, логирует каждый запрос (INFO) и ошибку (ERROR)
    return распарсенный json(dict/list) или None
    '''


    def delete(
            self,
            url: str,
            headers: Optional[Dict[str, str]]=None,
    ) -> Optional[Union[Dict[str, Any],list]]:
        try:
            response = requests.delete(url, headers=headers, timeout=10)
            response.raise_for_status()
            logger.info('DELETE ОК. URL: - %s, Code:  - %d', url, response.status_code)
            return response.json() if response.content else {}
        except requests.exceptions.RequestException as exc:
            logger.error('DELETE Error. - %s - %s', url, exc)
            return None

    def post(
            self,
            url: str,
            body: Dict[str, Any],
            headers:Optional[Dict[str, str]] = None,
    )-> Optional[Union[Dict[str, Any], list]]:
        default_headers = {
            'Accept': "application/json",
            'Content-Type': "application/json"
        }
        headers = headers or default_headers
        try:
            response = requests.post(url, data=json.dumps(body), headers=headers, timeout=10)
            response.raise_for_status()
            logger.info('POST ОК. URL: - %s, Code: - %d', url, response.status_code)
            return response.json()
        except requests.exceptions.RequestException as exc:
            logger.error('POST Error. - %s - %s', url, exc)
            return None

    def put(
            self,
            url: str,
            body: Dict[str, Any],
            headers: Optional[Dict[str, str]] = None,
    )-> Optional[Union[Dict[str, Any], list]]:
        default_headers = {
            'Accept': "application/json",
            'Content-Type': "application/json"
        }
        headers = headers or default_headers
        try:
            response = requests.put(url, data=json.dumps(body), headers=headers, timeout=10)
            response.raise_for_status()
            logger.info('PUT ОК. URL: - %s, Code: - %d', url, response.status_code)
            return response.json()
        except requests.exceptions.RequestException as exc:
            logger.error('PUT Error. - %s - %s', url, exc)
            return None

    def get(
            self,
            url: str,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            code=None,
    )-> Optional[Union[Dict[str, Any], list]]:
        response = requests.get(url, params=params, headers=headers)
        try:
            if code is None:
                response.raise_for_status()
            else:
                assert (response.status_code == code), f'Unexpected status {response.status_code}'
            logger.info('GET OK. URL: - %s, Code: - %d', url, response.status_code)
            return response.json() if response.content else {}
        except (requests.exceptions.RequestException, AssertionError) as exc:
            logger.error('GET Error. - %s - %s', url, exc)
            return None