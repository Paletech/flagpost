# from fastapi import File, UploadFile
import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


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

    class Config:
        orm_mode = True


class ImageUpload(BaseModel):
    pictures: List
