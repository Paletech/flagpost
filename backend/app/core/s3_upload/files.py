import os
from datetime import date
from uuid import uuid4

from app.core.s3_upload.base import BaseS3Manager, AbstractBaseS3ObjectManager
from app.db.models import User
from fastapi import UploadFile


class FileS3Object(AbstractBaseS3ObjectManager):
    """Class that manages file properties."""
    def set_filename(self, file: UploadFile, user: User):
        """Method that assign file name."""
        now = date.today()
        folder_from_now = "/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day) + "/"
        filename = user.id.hex + folder_from_now + uuid4().hex + self.get_file_type(filename=file.filename)
        return filename


class FileS3Manager(BaseS3Manager, FileS3Object):
    """Class that manages files in s3 bucket"""
    BUCKET_NAME = os.getenv("S3_FILE_BUCKET")
