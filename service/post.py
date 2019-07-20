from models import Post,Relationship
from models import db
from datetime import datetime, timezone
import boto3
from config import *
import errors
from sqlalchemy import desc
import service.relation

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
    result = db.session.query(Post).filter(Post.user_id == userid).order_by(desc(Post.created_at)).limit(10).all()
    return result

def GetNewPosts(userid):
    result = []

    #Get user's last post
    userspostsquery = db.session.query(Post).filter(Post.user_id == userid).order_by(desc(Post.created_at)).limit(1).all()
    if userspostsquery:
        post = {"username":"Me!!","post":"","createdate":""}
        post["post"] = userspostsquery[0].text
        post["createdate"] = userspostsquery[0].created_at
        result.append(post)

    # Then get user's friends posts
    # Get user friends first
    friends = service.relation.GetFriends(userid)
    for friend in friends:
        post = {"username":"","post":"","createdate":""}
        friendspostsquery = db.session.query(Post).filter(Post.user_id == friend.id).order_by(desc(Post.created_at)).limit(1).all()
        if friendspostsquery:
            post["username"] = friend.name
            post["post"] = friendspostsquery[0].text
            post["createdate"] = friendspostsquery[0].created_at
            result.append(post)

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


def LikePost(postid):
    post = db.session.query(Post).get(postid)
    if post:
        post.likes= post.likes + 1
        try:
            db.session.commit()
            return post.likes
        except Exception as error:
            return errors.internal_error(error)
