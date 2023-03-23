import os

from app.core.s3.upload.base import BaseS3Manager


class ImageS3Manager(BaseS3Manager):
    """Class that manages images in s3 bucket"""
    BUCKET_NAME = os.getenv("S3_IMAGE_BUCKET")
