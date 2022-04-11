import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from app.category.schemas import CategoryOut
from app.files.schemas import FileOut


class PostBase(BaseModel):
    type: str = None
    text: str = None


class PostOut(PostBase):
    id: UUID = None
    user_id: UUID = None
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None
    files: Optional[List[FileOut]] = []
    categories: Optional[List[CategoryOut]] = []

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    categories: Optional[List[UUID]] = None
    files: Optional[List[UUID]] = None
    #
    # class Config:
    #     orm_mode = True


class PostEdit(PostBase):
    # id: UUID
    categories: Optional[List[UUID]] = None
    files: Optional[List[UUID]] = None

    class Config:
        orm_mode = True
