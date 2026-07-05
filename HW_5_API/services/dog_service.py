from __future__ import annotations

from HW_5_API.helpers.base_service import BaseService
from HW_5_API.models.dog_api import DogApiResponse, DogApiListResponse


class DogService(BaseService):
    """обработка над https://dog.ceo/api"""

    BASE_URL = 'https://www.dog.ceo/api'

    @classmethod
    def list_all_breeds(cls) -> DogApiListResponse:
        raw = cls().get(f'{cls.BASE_URL}/breeds/list/all')
        # полученные данные парсим в DogApiListResponse
        return DogApiListResponse.parse_obj(raw)

    @classmethod
    def list_breeds(cls) -> DogApiListResponse:
        raw = cls().get(f'{cls.BASE_URL}/breeds/list')
        return DogApiListResponse.parse_obj(raw)

    @classmethod
    def sub_breeds(cls, breed: str) -> DogApiListResponse:
        raw = cls().get(f'{cls.BASE_URL}/breed/{breed}/list')
        return DogApiListResponse.parse_obj(raw)

    @classmethod
    def random_image(cls) -> DogApiResponse:
        raw = cls().get(f'{cls.BASE_URL}/breeds/image/random')
        return DogApiResponse.parse_obj(raw)

    @classmethod
    def random_image_by_breed(cls, breed: str) -> DogApiResponse:
        raw = cls().get(f'{cls.BASE_URL}/breed/{breed}/images/random')
        return DogApiResponse.parse_obj(raw)

    @classmethod
    def random_images(cls, count: int) -> DogApiListResponse:
        raw = cls().get(f'{cls.BASE_URL}/breeds/image/random/{count}')
        return DogApiListResponse.parse_obj(raw)
