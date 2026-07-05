from __future__ import annotations
from typing import Dict, Any

from HW_5_API.helpers.base_service import BaseService
from HW_5_API.models.jsonplaceholder_api import (PostBase, PostListModel, PostCreateResponse, )


class JsonPlaceholderService(BaseService):
    '''обаботка https://www.jsonplaceholder.typicode.com'''

    BASE_URL = 'https://www.jsonplaceholder.typicode.com'

    @classmethod
    def list_posts(cls) -> PostListModel:
        raw = cls().get(f'{cls.BASE_URL}/posts')
        return PostListModel.parse_obj(raw)

    @classmethod
    def get_post(cls, post_id: int) -> PostBase:
        raw = cls().get(f'{cls.BASE_URL}/posts/{post_id}')
        return PostBase.parse_obj(raw)

    @classmethod
    def create_post(cls, payload: Dict[str, Any]) -> PostCreateResponse:
        raw = cls().post(f'{cls.BASE_URL}/posts', body=payload)
        return PostCreateResponse.parse_obj(raw)

    @classmethod
    def update_post(cls, post_id: int, playload: Dict[str, Any]) -> None:
        raw = cls().put(f'{cls.BASE_URL}/posts/{post_id}', body=playload)
        return PostBase.parse_obj(raw)

    @classmethod
    def delete_post(cls, post_id: int) -> None:
        cls().delete(f'{cls.BASE_URL}/posts/{post_id}')