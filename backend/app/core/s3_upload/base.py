from datetime import date
from pathlib import Path
from typing import Union
from urllib.parse import urlparse
from uuid import uuid4

from app.core.s3_upload.abs import AbstractBaseS3Manager
from app.db.models import Files, Images, User
from fastapi import UploadFile


class BaseS3ObjectManager:
    """Class for base objects management such:
     get filename,
     set filename,
     get_suffix
     """

    def set_filename(self, user: User, file: UploadFile) -> str:
        """Method that assign file name."""
        now = date.today()
        folder_from_now = "/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day) + "/"
        filename = user.id.hex + folder_from_now + uuid4().hex + self.get_file_type(filename=file.filename)
        return filename

    @staticmethod
    def get_file_type(filename: str) -> str:
        """Method that returns file type (suffix)."""
        return Path(filename).suffix

    @staticmethod
    def get_object_id(image: Union[Images, Files]):
        """Method that returns uuid of s3 object from URL."""
        object_id = urlparse(image.path).path[1:]
        return object_id


class BaseS3Manager(AbstractBaseS3Manager, BaseS3ObjectManager):
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
