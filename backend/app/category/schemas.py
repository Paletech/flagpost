import datetime
from uuid import UUID

from pydantic import BaseModel

from app.image.schemas import ImageOut


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
    image: ImageOut = None

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
