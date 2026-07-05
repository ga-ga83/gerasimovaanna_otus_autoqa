"""тесты для https://dog.ceo/api"""

import pytest
from HW_5_API.services.dog_service import DogService
from HW_5_API.models.dog_api import DogApiResponse, DogApiListResponse

def test_all_breeds_success():
    model: DogApiListResponse = DogService.list_all_breeds()
    assert isinstance(model, DogApiResponse)
    assert 'hound' in model.message

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


@pytest.mark.parametrize('breed', ['hound', 'retriver', 'pug'])
def test_random_image_by_breed(breed):
    img: DogApiResponse = DogService.random_image_by_breed(breed)
    assert isinstance(img, DogApiResponse)
    assert img.message.lower().endswith((c))


def test_multiple_random_images():
    count = 5
    imgs: DogApiListResponse = DogService.random_images(count)
    assert isinstance(imgs, DogApiResponse)
    assert len(imgs.message) == count
    for url in imgs.message:
        assert isinstance(url, str)
        assert url.lower().endswith(('.jpg', '.jpeg', '.png'))

def test_hound_sub_breeds():
    subs: DogApiListResponse = DogService.sub_breeds('hound')
    assert isinstance(subs, DogApiListResponse)
    assert any(x in subs.message for x in ('afghan', 'basset', 'blood'))