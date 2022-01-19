import datetime

from pydantic import BaseModel
from pydantic.color import Color
import typing as t
from typing import List, Optional, Set

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

from app.image.schemas import ImageOut


class CategoryBase(BaseModel):
    name: str = None
    color: str = None


class CategoryOut(CategoryBase):
    id: int = None
    user_id: int = None
    category_id: int = None
    selected: int = None
    created_at: datetime.datetime = datetime.datetime.utcnow()
    updated_at: datetime.datetime = datetime.datetime.utcnow()
    image: Optional[ImageOut] = None

    class Config:
        orm_mode = True


class CategoryCreate(CategoryBase):
    image_id: str = None

    class Config:
        orm_mode = True


class CategoryEdit(CategoryBase):
    image_id: str = None

    class Config:
        orm_mode = True


# class User(JobBase):
#     id: int
#
#     class Config:
#         orm_mode = True

