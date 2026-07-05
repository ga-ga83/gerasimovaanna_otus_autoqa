'''тесты для https://jsonplaceholder.tupicode.com'''

import pytest
from HW_5_API.services.jsonplaceholder_service import JsonPlaceholderService


def test_posts_list():
    lst = JsonPlaceholderService.list_posts()
    assert len(lst.__root__) == 100
    first = lst.__root__[0]
    for attr in ('userId', 'id', 'title', 'body'):
        assert getattr(first, attr) is not None

@pytest.mark.parametrize('post_id', [1, 45, 100])
def test_get_single_post(post_id):
    post = JsonPlaceholderService.get_post(post_id)
    assert post.id == post_id
    assert isinstance(post.title, str) and post.title
    assert isinstance(post.body, str) and post.body

def test_create_post():
    payloard = {'title': 'foo', 'body': 'bar', 'uiserId': 1}
    created = JsonPlaceholderService.create_post(payloard)
    assert created.title == payloard['title']
    assert created.body == payloard['body']
    assert created.userId == payloard['userId']
    assert created.id == 101


@pytest.mark.parametrize('post_id, new_title',
                         [(1, 'updated title #1'), (42, 'the answeer'), (78, 'final post')],
                        )
def test_put_update(post_id, new_title):
    playload = {'id': post_id, 'title': new_title, 'body': 'unchander', 'userId': 1}
    upd = JsonPlaceholderService.update_post(post_id, playload)
    assert upd.id == post_id
    assert upd.title == new_title
    assert upd.body == 'unchander'


def test_delete_post():
    JsonPlaceholderService.delete_post(1)
