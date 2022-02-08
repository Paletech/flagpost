import secrets

import boto3
import requests
from fastapi import HTTPException, status


def upload_to_s3(file, user, post_id):

    s3_client = boto3.client(
        's3',
        aws_access_key_id="AKIAWJ7BVKE4ZH5TW4M7",
        aws_secret_access_key="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"
    )

    if post_id is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="post id is empty")

    file_name = (secrets.token_urlsafe(10) + '.').join(file.filename.split('.'))
    #Generate the presigned URL
    response = s3_client.generate_presigned_post(
        Bucket='fastapi-test-api',
        Key=f'{user.id}/{post_id}/{file_name}',
        ExpiresIn=10
    )
    data_for_base = response.pop('url') + response.get('fields').pop('key')

    return {'data_for_base': data_for_base, 'response': response}
