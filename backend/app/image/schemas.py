from uuid import UUID

from pydantic import BaseModel
import typing as t
import datetime


class ImageBase(BaseModel):
    path: str = None
    public_path: str = None


class ImageOut(ImageBase):
    id: UUID
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None

    class Config:
        orm_mode = True


class ImageCreate(ImageBase):
    path: str

    class Config:
        orm_mode = True
