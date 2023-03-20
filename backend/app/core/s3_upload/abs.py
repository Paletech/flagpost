import os
from abc import ABC, abstractmethod

from aioboto3 import Session
from fastapi import UploadFile

from app.db.session import Base


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
