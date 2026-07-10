from typing import Optional, List, Any
from pydantic import BaseModel, Field, field_validator, RootModel


class PostsBase(BaseModel):
    userId: int
    id: int
    title: str
    body: str


class CommentsBase(BaseModel):
    postId: int
    id: int
    name: str
    email: str
    body: str


class Album(BaseModel):
    userId: int
    id: int
    title: str

