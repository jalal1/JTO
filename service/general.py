import boto3
from config import *
import errors

def UploadImage(file):
    # upload to s3 code
    try:
        if file.data:
            s3_client = boto3.client(
            "s3",
            aws_access_key_id=Config.S3_KEY,
            aws_secret_access_key=Config.S3_SECRET
            )
            s3_client.upload_fileobj(file.data, Config.S3_BUCKET,file.data.filename)
            return "{}{}".format(Config.S3_LOCATION, file.data.filename)

    except Exception as error:
        return errors.internal_error(error)

