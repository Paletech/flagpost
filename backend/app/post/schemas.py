import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from app.category.schemas import CategoryOut


class PostBase(BaseModel):
    type: str = None
    text: str = None


class PostOut(PostBase):
    id: UUID = None
    user_id: int = None
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None
    category: Optional[List[CategoryOut]] = []
    # category: List[CategoryOut] = []

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    class Config:
        orm_mode = True


class PostEdit(PostBase):
    id: int

    class Config:
        orm_mode = True
