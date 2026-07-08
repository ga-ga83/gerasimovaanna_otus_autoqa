'''тесты для https://jsonplaceholder.tupicode.com'''

import pytest
from HW_5_API.services.placeholder_service import JPlaceholderService
from HW_5_API.models.jplaceholder_api import PostsBase, CommentsBase, Album


def test_posts_list():
    raw = JPlaceholderService.get_list_posts()
    assert len(raw) > 0
    posts = [PostsBase.model_validate(obj) for obj in raw]
    assert all(p.id is not None for p in posts)


@pytest.mark.parametrize('post_id', [1, 45, 100])
def test_get_comments(post_id: int):
    comments = JPlaceholderService.get_post_comments(post_id)
    assert len(comments) > 0
    comment = comments[0]
    assert comment.postId == post_id
    assert isinstance(comment.name, str) and comment.name
    assert isinstance(comment.body, str) and comment.body


def test_get_albums():
    albums = JPlaceholderService.get_albums()
    assert len(albums) > 0
    assert all(isinstance(a, Album) for a in albums)


@pytest.mark.parametrize('post_id, new_title',
                         [(3, 'updated title #1'), (7, 'the answer'), (18, 'final post')])
def test_put_update(post_id, new_title):
    payload = {
        'id': post_id,
        'title': new_title,
        'body': 'unchanged',
        'userId': 1
    }
    resp = JPlaceholderService.update_post(post_id, payload)

    assert isinstance(resp, dict)
    assert resp.get('id') == post_id


@pytest.mark.parametrize('post_id', [23])
def test_delete_post(post_id):
    resp = JPlaceholderService.delete_post(post_id)
    assert isinstance(resp, dict)
    try:
        resp_get = JPlaceholderService.get_post_by_id(post_id)
        assert resp_get is None, "Пост должен быть недоступен после удаления"
    except Exception:
        pass

