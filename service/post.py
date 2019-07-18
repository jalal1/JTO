from models import Post
from models import db
from datetime import datetime, timezone
import boto3
from config import *
import errors
from sqlalchemy import desc

def AddPost(text,userid):

    try:
        post = Post()
        post.text = text
        post.user_id = userid

        db.session.add(post)
        db.session.commit()

        return "Post added successfully!!"
    except Exception as error:
        return errors.internal_error(error)


def GetPostById(id):
    result = Post.query.get(id)
    return result

def Getlast10posts(userid):
    result = db.session.query(Post).filter(Post.user_id == userid).order_by(desc(Post.created_at)).limit(5).all()
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
