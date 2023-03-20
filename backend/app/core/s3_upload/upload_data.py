import os
from uuid import uuid4, UUID
from app.core.s3_upload.base import BaseS3Manager, BaseS3Object


def upload_to_s3():
    pass


class FileS3Manager(BaseS3Manager, BaseS3Object):
    def set_filename(self, **kwargs):
        pass

    async def delete(self, object_key):
        pass

    async def upload(self, file):
        pass

# def upload_to_s3(file, user, post_id):
#
#     s3_client = boto3.client(
#         's3',
#         aws_access_key_id="AKIAWJ7BVKE4ZH5TW4M7",
#         aws_secret_access_key="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"
#     )
#
#     if post_id is None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="post id is empty")
#
#     file_name = (secrets.token_urlsafe(10) + '.').join(file.filename.split('.'))
#     # Generate the presigned URL
#     response = s3_client.generate_presigned_post(
#         Bucket='fastapi-test-api',
#         Key=f'{user.id}/{post_id}/{file_name}',
#         ExpiresIn=10
#     )
#     data_for_base = response.pop('url') + response.get('fields').pop('key')
#
#     return {'data_for_base': data_for_base, 'response': response}
