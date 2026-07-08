import requests
from HW_5_API.helpers.base_service import BaseService
from HW_5_API.models.dog_api import DogApiResponse, DogApiListResponse, DogApiBreedsListResponse


class DogService(BaseService):
    BASE_URL = "https://dog.ceo/api"

    @classmethod
    def _request(cls, path: str) -> dict:
        if not path.startswith("/"):
            path = "/" + path
        url = f"{cls.BASE_URL}{path}"

        resp = requests.get(
            url,
            headers=cls._default_headers(),
            timeout=10,
        )
        resp.raise_for_status()  # выбросит HTTPError для 4xx/5xx

        data = resp.json()
        if data.get("status") != "success":
            raise RuntimeError(f"Dog API error: {data}")
        return data

    @classmethod
    def list_all_breeds(cls) -> DogApiBreedsListResponse:
        raw = cls._request("/breeds/list/all")
        return DogApiBreedsListResponse.model_validate(raw)

    @classmethod
    def list_breeds(cls) -> DogApiListResponse:
        raw = cls._request("/breeds/list")
        return DogApiListResponse(**raw)

    @classmethod
    def sub_breeds(cls, breed: str) -> DogApiListResponse:
        raw = cls._request(f"/breed/{breed}/list")
        return DogApiListResponse(**raw)

    @classmethod
    def random_image(cls) -> DogApiResponse:
        raw = cls._request("/breeds/image/random")
        return DogApiResponse(**raw)

    @classmethod
    def random_image_by_breed(cls, breed: str) -> DogApiResponse:
        raw = cls._request(f"/breed/{breed}/images/random")
        return DogApiResponse(**raw)

    @classmethod
    def random_images(cls, count: int) -> DogApiListResponse:
        if count <= 0:
            return DogApiListResponse(message=[], status="success")

        images = []
        for _ in range(count):
            img = cls.random_image()
            images.append(img.message)
        return DogApiListResponse(message=images, status="success")

