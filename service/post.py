from models import PostModel
from models import db
from datetime import datetime, timezone
import boto3
from config import *


def AddPost(text):

    try:
        post = PostModel()
        post.text = text

        db.session.add(post)
        db.session.commit()

        return "Post added successfully!!"
    except Exception as error:
        db.session.rollback()
        return error


def GetPostById(id):
    result = PostModel.query.get(id)
    return result


def UploadImage(file_to_upload):
    # upload to s3 code
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=Config.S3_KEY,
        aws_secret_access_key=Config.S3_SECRET
    )
    #s3_client.upload_fileobj(file_to_upload, Config.S3_BUCKET,file_to_upload.filename)

    return 'done'
