import os

from app.core.s3_upload.base import BaseS3Manager


class FileS3Manager(BaseS3Manager):
    """Class that manages files in s3 bucket"""
    BUCKET_NAME = os.getenv("S3_FILE_BUCKET")
