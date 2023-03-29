import datetime
import typing as t
from uuid import UUID

from pydantic import BaseModel


class FileBase(BaseModel):
    width: int = None
    height: int = None
    path: str = None
    public_path: str = None


class FileOut(FileBase):
    id: UUID
    post_id: UUID = None
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None

    class Config:
        orm_mode = True


class FileCreate(FileBase):
    post_id: UUID = None

    class Config:
        orm_mode = True


class FileUpload(BaseModel):
    post_id: UUID

    # class Config:
    #     orm_mode = True
    #

class FileEdit(FileBase):
    id: UUID

    class Config:
        orm_mode = True
