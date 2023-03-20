import os
from uuid import uuid4

from app.core.s3_upload.base import BaseS3Manager, AbstractBaseS3ObjectManager
from app.db.models import User
from fastapi import UploadFile


class ImageS3ObjectManager(AbstractBaseS3ObjectManager):
    """Class that manages image properties."""
    def set_filename(self, file: UploadFile, user: User) -> str:
        """Method that sets the file name."""
        filename = user.id.hex + "/" + uuid4().hex + self.get_file_type(filename=file.filename)
        return filename


class ImageS3Manager(BaseS3Manager, ImageS3ObjectManager):
    """Class that manages images in s3 bucket"""
    BUCKET_NAME = os.getenv("S3_IMAGE_BUCKET")
