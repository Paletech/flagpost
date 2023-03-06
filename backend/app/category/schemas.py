import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic.color import Color
import typing as t
from typing import List, Optional, Set

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl, Field

from app.image.schemas import ImageOut, ImageBase


class CategoryBase(BaseModel):
    name: str = None
    color: str = None


class CategoryOut(CategoryBase):
    id: UUID = None
    user_id: UUID = None
    category_id: UUID = None
    selected: int = None
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None
    # image_id: Optional[ImageBase] = []
    # image_id: ImageOut = []
    # image_id: Optional[ImageBase] = []
    # image_id: Optional[ImageOut] = Field(default=None, foreign_key="images.id")
    # image_id: ImageOut = Field(default=None, foreign_key="images.id")
    # image_id: UUID # TODO
    # image_id: ImageOut

    class Config:
        orm_mode = True


class CategoryCreate(CategoryBase):
    image_id: UUID = None

    class Config:
        orm_mode = True


class CategoryEdit(CategoryBase):
    image_id: UUID = None

    class Config:
        orm_mode = True


# class User(JobBase):
#     id: int
#
#     class Config:
#         orm_mode = True

