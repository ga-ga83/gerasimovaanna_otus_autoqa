from __future__ import annotations
from typing import Dict, Any, Optional

from HW_5_API.helpers.base_service import BaseService
from HW_5_API.models.brewerydb import BreweryResponse, BreweryListResponse, MetaResponse

class BreweryService(BaseService):
    "API https://api.openbrewerydb.org"

    BASE_URL = 'https://api.openbrewerydb.org/breweries'

    #список пивоварен
    @classmetod
    def list_all(
        cls,
        params: Optional[Dict[str, Any]] = None,
    ) -> BreweryResponse:
        raw = cls().get(cls.BASE_URL, params=params or {})
        #полученные данные парсим в BreweryListResponse
        return BreweryListResponse.parse_obj(raw)

    #одна пивоварня по ее ID
    @classmethod
    def get_by_id(cls, brewery_id: str) -> BreweryResponse:
        raw = cls().get(f'{cls.BASE_URL}/{brewery_id}')
        return BreweryResponse.parse_obj(raw)

    #произвольный запрос списка
    @classmethod
    def search(cls, querty: str) -> BreweryListResponse:
        raw = cls().get(f'{cls.BASE_URL}/search', params={"querty": querty})
        return BreweryListResponse.parse_obj(raw)

    #получение мета-данных
    @classmethod
    def get_meta_from_headers(cls, response_headers: Dict[str, str]) -> MetaResponse:
        total = int(response_headers.get('Total', '0'))
        page = int(response_headers.get('Page', '1'))
        per_page = int(response_headers.get('Per-Page', '20'))
        return MetaResponse(total=total, page=page, per_page=per_page)
