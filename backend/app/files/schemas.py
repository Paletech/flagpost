import datetime
from uuid import UUID

from pydantic import BaseModel
import typing as t


class FileBase(BaseModel):
    width: int = None
    height: int = None
    path: str = None
    public_path: str = None


class FileOut(FileBase):
    id: int
    post_id: UUID = None
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None

    class Config:
        orm_mode = True


class FileCreate(FileBase):
    post_id: UUID = None

    class Config:
        orm_mode = True


class FileEdit(FileBase):
    id: int

    class Config:
        orm_mode = True
