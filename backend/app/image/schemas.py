from fastapi import File, UploadFile
from typing import Optional, List, Dict
from uuid import UUID
from pydantic import BaseModel
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

    class Config:
        orm_mode = True


class ImageUpload(BaseModel):
    # file = File
    # file: Optional[UploadFile] = File(...)
    pictures: List
    # pictures: str
    # pictures: Dict



