from __future__ import annotations
from typing import List

from pydantic import BaseModel, validator, Field

class PostBase(BaseModel):
    userId: int
    id_: int
    title: str
    body: str

    @validator('title', 'body')
    def not_blank(cls, v):
        if not v.strip():
            raise ValueError('must not be empty')
        return v

class PostListModel(BaseModel):
    __root__: List[PostBase]


class PostCreateResponse(PostBase):
    """POST / posts возвращает id = 101 (константа)"""
    id_: int = Field(..., const=True)