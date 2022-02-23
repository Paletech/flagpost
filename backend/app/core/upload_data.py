import secrets
from aiobotocore.session import get_session
import aioboto3
from fastapi import HTTPException, status

from app.core.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME

#
# def upload_to_s3(file, user, post_id):
#
#     s3_client = boto3.client(
#         's3',
#         aws_access_key_id=AWS_ACCESS_KEY_ID,
#         aws_secret_access_key=AWS_SECRET_ACCESS_KEY
#     )
#
#     if post_id is None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="post id is empty")
#
#     file_name = (secrets.token_urlsafe(10) + '.').join(file.filename.split('.'))
#     #Generate the presigned URL
#     response = s3_client.generate_presigned_post(
#         Bucket=AWS_STORAGE_BUCKET_NAME,
#         Key=f'{user.id}/{post_id}/{file_name}',
#         ExpiresIn=10
#     )
#     data_for_base = response.pop('url') + response.get('fields').pop('key')
#
#     return {'data_for_base': data_for_base, 'response': response}
#
#
# def upload_image_to_s3(file, filename):
#
#     file_name = (secrets.token_urlsafe(10) + '.' + filename.split(".")[-1])
#
#     # s3_client = boto3.client(
#     #     's3',
#     #     aws_access_key_id="AKIAWJ7BVKE4ZH5TW4M7",
#     #     aws_secret_access_key="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"
#     # )
#
#     s3 = boto3.resource('s3',
#                         aws_access_key_id=AWS_ACCESS_KEY_ID,
#                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
#
#     image_base64 = file
#     obj = s3.Object(AWS_STORAGE_BUCKET_NAME, f"image/{file_name}")
#     obj.put(Body=image_base64)
#     # location = s3_client.get_bucket_location(Bucket='fastapi-test-api')['LocationConstraint']
#     object_url = "https://%s.s3.amazonaws.com/%s" % (AWS_STORAGE_BUCKET_NAME, f"image/{file_name}")
#     return object_url
#
#
# def delete_file_from_s3(filename):
#     file = filename.split('/')[-1]
#     s3_client = boto3.client(
#         's3',
#         aws_access_key_id=AWS_ACCESS_KEY_ID,
#         aws_secret_access_key=AWS_SECRET_ACCESS_KEY
#     )
#     s3_client.delete_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=f"image/{file}")


async def upload_to_s3(file, user, post_id):

    if post_id is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="post id is empty")

    session = get_session()
    async with session.create_client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    ) as client:

        file_name = (secrets.token_urlsafe(10) + '.').join(file.filename.split('.'))

        response = await client.generate_presigned_post(
            Bucket=AWS_STORAGE_BUCKET_NAME,
            Key=f'{user.id}/{post_id}/{file_name}',
            ExpiresIn=10
        )
        data_for_base = response.pop('url') + response.get('fields').pop('key')

        return {'data_for_base': data_for_base, 'response': response}


async def upload_image_to_s3(file, filename):

    file_name = (secrets.token_urlsafe(10) + '.' + filename.split(".")[-1])
    session = aioboto3.Session()

    async with session.resource('s3',
                                aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY) as s3:

        image_base64 = file
        obj = await s3.Object(AWS_STORAGE_BUCKET_NAME, f"image/{file_name}")
        await obj.put(Body=image_base64)
        # location = s3_client.get_bucket_location(Bucket='fastapi-test-api')['LocationConstraint']
        object_url = "https://%s.s3.amazonaws.com/%s" % (AWS_STORAGE_BUCKET_NAME, f"image/{file_name}")
        return object_url


async def delete_file_from_s3(filename):
    file = filename.split('/')[-1]

    session = aioboto3.Session()

    async with session.resource('s3',
                                aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY) as s3:

        bucket = await s3.Bucket(AWS_STORAGE_BUCKET_NAME)
        await bucket.objects.filter(Prefix=f"image/{file}").delete()
