from typing import Dict, Any, Optional

from HW_5_API.helpers.base_service import BaseService
from HW_5_API.models.brewerydb import BreweryResponse, BreweryListResponse, MetaResponse


class BreweryService(BaseService):
    """API https://api.openbrewerydb.org/v1/breweries"""

    BASE_URL = "https://api.openbrewerydb.org/v1/breweries"

    @classmethod
    def list_all(cls, params: Optional[Dict[str, Any]] = None) -> BreweryListResponse:
        raw = cls().get(cls.BASE_URL, params=params or {})
        if raw is None:
            raw = []
        return BreweryListResponse(data=[BreweryResponse.model_validate(item) for item in raw])

    @classmethod
    def get_by_id(cls, brewery_id: str) -> BreweryResponse:
        raw = cls().get(f"{cls.BASE_URL}/{brewery_id}")
        return BreweryResponse.model_validate(raw)

    @classmethod
    def search(cls, query: str) -> BreweryListResponse:
        url = "https://api.openbrewerydb.org/v1/breweries/search"
        raw = cls().get(url, params={"query": query})
        if raw is None:
            raw = []
        return BreweryListResponse(
            data=[BreweryResponse.model_validate(item) for item in raw]
        )

    @classmethod
    def get_meta_from_headers(cls, response_headers: Dict[str, str]) -> MetaResponse:
        total = int(response_headers.get("total", "0"))
        page = int(response_headers.get("page", "1"))
        per_page = int(response_headers.get("per_page", "20"))
        return MetaResponse(total=total, page=page, per_page=per_page)
