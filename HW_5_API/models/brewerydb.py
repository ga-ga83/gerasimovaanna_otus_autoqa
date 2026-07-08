from typing import Optional, List, Any

from pydantic import BaseModel, Field, field_validator, RootModel


class BreweryResponse(BaseModel):
    id: str
    name: str
    brewery_type: str
    street: Optional[str] = None
    address_1: Optional[str] = None
    address_2: Optional[str] = None
    address_3: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    phone: Optional[str] = None
    website_url: Optional[str] = None


class BreweryListResponse(BaseModel):
    data: List[BreweryResponse]


class MetaResponse(BaseModel):
    total: str = Field(strict=True)
    page: str = Field(strict=True)
    per_page: str = Field(strict=True)
