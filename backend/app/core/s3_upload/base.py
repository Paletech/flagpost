import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union
from urllib.parse import urlparse

from aioboto3 import Session
from app.db.models import Files, Images, User
from app.db.session import Base
from fastapi import UploadFile


class AbstractBaseS3ObjectManager(ABC):
    """Class for base objects management such:
     get filename,
     set filename,
     get_suffix
     """
    @abstractmethod
    def set_filename(self, **kwargs):
        """Abstract method that assign file name."""
        pass

    @classmethod
    def get_file_type(cls, filename: str) -> str:
        """Method that returns file type (suffix)."""
        return Path(filename).suffix

    @staticmethod
    def get_object_id(image: Union[Images, Files]):
        """Method that returns uuid of s3 object from URL."""
        object_id = urlparse(image.path).path[1:]
        return object_id


class AbstractBaseS3Manager(ABC):
    """Base Abstract class that manages interaction with s3 bucket."""
    __session = Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    BASE_BUCKET_URL_PATTERN = "https://{0}.s3.amazonaws.com/{1}"

    @classmethod
    async def upload_object(cls, file, bucket: str, filename: str) -> None:
        """Async method that uploads object to s3 bucket."""
        async with cls.__session.client("s3") as s3:
            await s3.upload_fileobj(file, bucket, filename)

    @classmethod
    async def delete_object(cls,  bucket: str, object_key: str) -> None:
        """Abstract method that deletes object from s3 bucket."""
        async with cls.__session.client("s3") as s3:
            await s3.delete_object(Bucket=bucket, Key=object_key)

    @abstractmethod
    async def upload(self, file: UploadFile) -> str:
        """Abstract method that uploads object to s3 bucket."""
        pass

    @abstractmethod
    async def delete(self, file_object: Base):
        """Abstract method that deletes object from s3 bucket."""
        pass


class BaseS3Manager(AbstractBaseS3Manager, AbstractBaseS3ObjectManager, ABC):
    """Base s3 manager class."""
    BUCKET_NAME = None

    def __init__(self, user: User):
        """Initialization of the necessary data"""
        self._user = user

    async def upload(self, file: UploadFile) -> str:
        """Method that uploads images to s3 bucket and returns image url path."""
        filename = self.set_filename(file=file, user=self._user)
        await self.upload_object(
            file.file,
            self.BUCKET_NAME,
            filename
        )
        return self.BASE_BUCKET_URL_PATTERN.format(self.BUCKET_NAME, filename)

    async def delete(self, file: Union[Files, Images]) -> None:
        file_id = self.get_object_id(file)
        await self.delete_object(
            bucket=self.BUCKET_NAME,
            object_key=file_id
        )
