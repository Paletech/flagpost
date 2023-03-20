import os
from uuid import uuid4, UUID

from app.core.s3_upload.base import BaseS3Manager, BaseS3Object


class ImageS3Object(BaseS3Object):
    """Class that manages я image properties."""
    def set_filename(self, file, user) -> str:
        """Method that sets the file name."""
        filename = user.id.hex + "/" + uuid4().hex + self.get_file_type(filename=file.filename)
        return filename


class ImageS3Manager(BaseS3Manager, ImageS3Object):
    """Class that manages images in s3 bucket"""

    def __init__(self, user):
        self.user = user
        self.BUCKET_NAME = os.getenv("S3_IMAGE_BUCKET")

    async def upload(self, file) -> str:
        """Method that uploads images to s3 bucket and returns image url path."""
        filename = self.set_filename(file=file, user=self.user)
        await self.upload_object(
            file.file,
            self.BUCKET_NAME,
            filename
        )
        return self.BASE_BUCKET_URL_PATTERN.format(self.BUCKET_NAME, filename)

    async def delete(self, image_id: UUID):
        await self.delete_object(
            bucket=self.BUCKET_NAME,
            object_key=self.user.id.hex + "/" + image_id
        )

