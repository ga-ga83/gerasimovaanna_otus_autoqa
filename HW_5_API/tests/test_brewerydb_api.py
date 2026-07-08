'''Тесты для https://www.openbrewerydb.org'''

import pytest
from HW_5_API.services.brewerydb_service import BreweryService
from HW_5_API.models.brewerydb import BreweryResponse, MetaResponse, BreweryListResponse


# список первой страницы
def test_first_page_is_not_empty():
    data: BreweryListResponse = BreweryService.list_all()
    assert len(data.data) > 0, "Список пивоварен пуст"

    # берём первую запись
    first = data.data[0]

    assert isinstance(first, BreweryResponse)
    for key in ("id", "name", "brewery_type", "city", "state", "country"):
        assert getattr(first, key) is not None, f"Поле {key} отсутствует у первой записи"


# тест пагинации (per_page = 5, 10, 20)
@pytest.mark.parametrize('per_page', [5, 10, 20])
def test_pagination(per_page):
    data: BreweryListResponse = BreweryService.list_all(params={"per_page": per_page})

    # Проверяем, что количество элементов равно запрошенному
    assert len(data.data) == per_page

    # Проверяем валидность каждого элемента списка
    for brew in data.data:
        assert isinstance(brew, BreweryResponse)


# тест по параметризации списка по городам/штатам
@pytest.mark.parametrize(
    "params,value,field",
    [
        ("by_city", "San Diego", "city"),
        ("by_city", "New York", "city"),
    ],
)
def test_filter_city_state(params, value, field):
    data: BreweryResponse = BreweryService.list_all(params={params: value})
    assert len(data.data) > 0, f"Нет результатов для фильтра {params}={value}"
    assert any(getattr(item, field) == value for item in data.data), \
        f"В результатах нет значения {value} в поле {field}"


def test_search_query():
    results: BreweryListResponse = BreweryService.search("san")
    assert len(results.data) > 0, "Поиск не вернул результатов"


# тест получения отдельной записи по ID
def test_get_by_known_id():
    known_id = "5fffcb8c-fbca-4633-8ef4-7bfd7dd6d473"
    brew: BreweryResponse = BreweryService.get_by_id(known_id)
    assert brew.id == known_id
    assert brew.name
    assert brew.website_url is not None
