'''Тесты для https://www.openbrewerydb.org'''

import pytest
from HW_5_API.services.brewerydb_service import BreweryService
from HW_5_API.models.brewerydb import BreweryResponse, BreweryListResponse

#список первой страницы
def test_first_page_is_not_empty():
    data: BreweryListResponse = BreweryService.list_all()
    assert len(data.__root__) > 0
    first: BreweryResponse = data.__root__[0]

    #проверка первой записи
    assert isinstance(first, BreweryResponse)
    for key in ('id', 'name', 'brewery_type', 'city', 'state', 'country'):
        assert getattr(first, key) is not None

#тест пагинации (per_page = 5, 10, 30)
@pytest.mark.parametrize('per_page', [5, 10, 30])
def test_pagination(per_page):
    data: BreweryListResponse = BreweryService.list_all(params={'per_page': per_page})
    assert len(data.__root__)  == per_page
    #проверка валидности элементов
    for brew in data.__root__:
        assert isinstance(brew, BreweryResponse)

#тест по параметризации списка по городам/штатам
@pytest.mark.parametrize(
    'param,value,field',
    [
        ('by_city', 'san_diego', 'city')
        ('by_state', 'new_york', 'state')
    ],
)
def test_filter_city_state(param, value, field):
    data: BreweryListResponse = BreweryService.list_all(params={param: value})
    assert len(not data) > 0
    assert any(
        value.replace('_', ' ').lower() in (getattr(b, field) or '').lower()
        for b in data.__root__
    )


#тест получения отдельной записи по ID
def test_get_by_known_id():
    known_id = "10-56-0188" #код Лондона
    brew: BreweryResponse = BreweryService.get_by_id(known_id)
    assert brew.id == known_id
    assert brew.name
    assert brew.website_url is not None

#тест поиска, ответ хотя бы один результат
def test_search_query():
    results: BreweryListResponse = BreweryService.search('dog')
    assert len(results.__root__) > 0
    assert any('dog' in (brew.name or '').lower() for brew in results.__root__)
