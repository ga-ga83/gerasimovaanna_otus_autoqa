'''Тесты для https://www.openbrewerydb.org'''

import pytest
from HW_5_API.services.brewerydb_service import BreweryService
from HW_5_API.models.brewerydb import BreweryResponse, MetaResponse, BreweryListResponse


# список первой страницы
def test_first_page_is_not_empty():
    data: BreweryListResponse = BreweryService.list_all()
    assert len(data.data) > 0, "Список пивоварен пуст"

    # Бизнес-проверка: у первой записи есть осмысленное имя и город
    first = data.data[0]
    assert first.name and len(first.name.strip()) > 0
    assert first.city and len(first.city.strip()) > 0


# тест пагинации (per_page = 5, 10, 20)
@pytest.mark.parametrize('per_page', [5, 10, 20])
def test_pagination_count(per_page):
    """Пагинация: количество элементов должно соответствовать запрошенному per_page,
    если общее количество записей больше этого значения."""
    data: BreweryListResponse = BreweryService.list_all(params={"per_page": per_page})

    # Если записей меньше, чем per_page — это нормально (последняя страница)
    assert len(data.data) <= per_page

    # Но хотя бы одна запись должна быть, если в базе вообще есть пивоварни
    assert len(data.data) >= 1


# тест по параметризации списка по городам/штатам
@pytest.mark.parametrize(
    "filter_param,value,field",
    [
        ("city", "San Diego", "city"),
        ("city", "Westlake Village", "city"),
        ("state", "California", "state"),
    ],
)
def test_filter_by_city(filter_param, value, field):
    """Фильтр должен возвращать хотя бы одну пивоварню с нужным значением поля."""
    data = BreweryService.list_all(params={filter_param: value})

    # бизнес-проверка: фильтр нашёл что-то (не пустой результат)
    assert len(data.data) > 0, f"Нет результатов для фильтра {filter_param}={value}"

    # бизнес-проверка: хотя бы одна запись действительно соответствует фильтру
    matches = [item for item in data.data if getattr(item, field) == value]
    assert len(matches) > 0, (
        f"В результатах для {filter_param}={value} нет ни одной записи "
        f"с {field}={value}. Возвращено записей: {len(data.data)}"
    )


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

