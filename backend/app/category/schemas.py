import datetime

from pydantic import BaseModel
from pydantic.color import Color
import typing as t


class CategoryBase(BaseModel):
    # user_id: int
    # image_id: int
    name: str = None
    color: Color = None # ошибка


class CategoryOut(CategoryBase):
    id: int
    # user_id: int
    # image_id: int
    category_id: int = None
    selected: int = None
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None

    class Config:
        orm_mode = True


class CategoryCreate(CategoryBase):
    class Config:
        orm_mode = True


class CategoryEdit(CategoryBase):
    id: int

    class Config:
        orm_mode = True


# class User(JobBase):
#     id: int
#
#     class Config:
#         orm_mode = True

