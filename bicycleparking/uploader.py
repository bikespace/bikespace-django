import boto3
import uuid
import os.path
from django.conf import settings


class Uploader:
    """This class is used for upload picture to S3"""

    def __init__(self):
        print(settings.AWS_ACCESS_KEY_ID)
        self.client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    def toS3(self, filename, file):
        key = str(uuid.uuid1())+os.path.splitext(filename)[1]
        self.client.put_object(Bucket=settings.S3_BUCKET,
                               Key=key,
                               Body=file.read())
        return key
