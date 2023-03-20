import os
from abc import abstractmethod, ABC
from pathlib import Path
from uuid import UUID

from aioboto3 import Session


class BaseS3Object:
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
    def get_object_id(path: str):
        """Method that returns uuid of s3 object from URL."""
        object_id = path.split('/')[-1]
        return object_id


class BaseS3Manager(ABC):
    """Base class that manages interaction with s3 bucket."""
    __session = Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    BASE_BUCKET_URL_PATTERN = "https://{0}.s3.amazonaws.com/{1}"

    @classmethod
    async def upload_object(cls, file, bucket: str, filename: str):
        """Async method that uploads object to s3 bucket."""
        async with cls.__session.client("s3") as s3:
            await s3.upload_fileobj(file, bucket, filename)

    @classmethod
    async def delete_object(cls,  bucket: str, object_key: UUID):
        """Abstract method that deletes object from s3 bucket."""
        async with cls.__session.client("s3") as s3:
            await s3.delete_object(Bucket=bucket, Key=object_key)

    @abstractmethod
    async def upload(self, file):
        """Abstract method that uploads object to s3 bucket."""
        pass

    @abstractmethod
    async def delete(self, object_key):
        """Abstract method that deletes object from s3 bucket."""
        pass
