from __future__ import annotation

from typing import Optional, List

from pydantic import BaseModel, Field, field_validator


class BreweryResponse(BaseModel):
    id_: str = Field(alias='id', strict=True)
    name: str = Field(strict=True)
    brewery_type: str = Field(strict=True)
    addres_1: Optional[str] = Field(defauli=None, strict=True)
    addres_2: Optional[str] = Field(defauli=None, strict=True)
    addres_3: Optional[str] = Field(defauli=None, strict=True)

    city: str = Field(strict=True)
    state_provice: str = Field(strict=True)
    country: str = Field(strict=True)
    state: str = Field(strict=True)
    street: str = Field(strict=True)

    longitude: Optional[str] = Field(defauli=None, strict=True)
    latitude: Optional[str] = Field(defauli=None, strict=True)

    phone: Optional[str] = Field(defauli=None, strict=True)
    website_url: Optional[str] = Field(defauli=None, strict=True)

    @field_validator(brewery_type)
    @classmethod
    def drewery_type_must_be_known(cls, value: str) -> str:
        """
        API перечисляет типы: micro, regional, brewpub, large, planning, bar,
        contract, proprietor, closed. Если получили неизвестный тип - выводим ошибку
        """
        known = {
            'micro',
            'regional',
            'brewpub',
            'large',
            'planning',
            'bar',
            'contract',
            'proprietor',
            'closed',
        }
        if value not in known:
            raise ValueError(f'unknown brewery_type: {value}')
        return value


class BreweryListResponse(BaseModel):
    """API может вернуть пустой массив"""
    __root__: List[BreweryResponse]


class MetaResponse(BaseModel):
    total: str = Field(strict=True)
    page: str = Field(strict=True)
    per_page: str = Field(strict=True)
