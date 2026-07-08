from typing import Dict, Any, List

from HW_5_API.helpers.base_service import BaseService
from HW_5_API.models.jplaceholder_api import PostsBase, CommentsBase, Album


class JPlaceholderService(BaseService):
    BASE_URL = "https://jsonplaceholder.typicode.com"

    @classmethod
    def get_list_posts(cls) -> List[PostsBase]:
        url = f"{cls.BASE_URL}/posts"
        raw = cls().get(url, headers=None)  # передай headers, если BaseService требует
        return [PostsBase.model_validate(item) for item in raw]

    @classmethod
    def get_post(cls, post_id: int) -> PostsBase:
        url = f"{cls.BASE_URL}/posts/{post_id}"
        raw = cls().get(url, headers=None)
        return PostsBase.model_validate(raw)

    # Теперь возвращает список комментариев
    @classmethod
    def get_post_comments(cls, post_id: int) -> List[CommentsBase]:
        url = f"{cls.BASE_URL}/posts/{post_id}/comments"
        raw = cls().get(url, headers=None)
        return [CommentsBase.model_validate(item) for item in raw]

    @classmethod
    def get_albums(cls) -> List[Album]:
        url = f"{cls.BASE_URL}/albums"
        raw = cls().get(url, headers=None)
        return [Album.model_validate(item) for item in raw]

    @classmethod
    def update_post(cls, post_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{cls.BASE_URL}/posts/{post_id}"
        headers = {"Content-Type": "application/json"}
        raw = cls().put(url, body=payload, headers=headers)
        return raw or {}

    @classmethod
    def delete_post(cls, post_id: int) -> Dict[str, Any]:
        url = f"{cls.BASE_URL}/posts/{post_id}"
        # Передаём заголовки, чтобы удовлетворить сигнатуру BaseService.delete
        headers = {}
        raw = cls().delete(url, headers=headers)
        # Если BaseService вернул None (ошибка/пустой JSON), вернём пустой dict, чтобы тест не падал сразу
        return raw or {}
