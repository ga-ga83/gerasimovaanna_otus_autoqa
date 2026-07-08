"""тесты для https://dog.ceo/api"""

import pytest
from HW_5_API.services.dog_service import DogService
from HW_5_API.models.dog_api import DogApiResponse, DogApiListResponse, DogApiBreedsListResponse


def test_all_breeds_success() ->DogApiBreedsListResponse:
    model = DogService.list_all_breeds()
    assert isinstance(model, DogApiBreedsListResponse)
    assert model.status == "success"
    assert isinstance(model.message, dict)
    assert len(model.message) > 0

@pytest.mark.parametrize(
    'func,expected_model',
    [
        (DogService.list_breeds, DogApiListResponse),
        (lambda: DogService.sub_breeds('hound'), DogApiListResponse),
        (DogService.random_image, DogApiResponse),
    ],
)
def test_simple_endpoints(func, expected_model):
    result = func()
    assert isinstance(result, expected_model)
    assert result.status == 'success'


@pytest.mark.parametrize('breed', ['hound', 'retriever', 'pug'])
def test_random_image_by_breed(breed):
    img = DogService.random_image_by_breed(breed)
    assert isinstance(img, DogApiResponse)
    assert img.status == "success"

    url = img.message  # в DogApiResponse поле message содержит URL картинки
    assert url.lower().endswith(".jpg") or url.lower().endswith(".png")


def test_multiple_random_images():
    count = 5
    imgs = DogService.random_images(count)
    assert isinstance(imgs, DogApiListResponse)
    assert imgs.status == "success"
    assert isinstance(imgs.message, list)
    assert len(imgs.message) == count
    for url in imgs.message:
        assert url.startswith("http")
        assert url.lower().endswith((".jpg", ".png"))


def test_hound_sub_breeds():
    subs: DogApiListResponse = DogService.sub_breeds('hound')
    assert isinstance(subs, DogApiListResponse)
    assert any(x in subs.message for x in ('afghan', 'basset', 'blood'))
