from models import PostModel
from models import db
from datetime import datetime, timezone


def AddPost(text):

    try:
        post = PostModel()
        post.text = text
        post.created_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")

        db.session.add(post)
        db.session.commit()

        return "Post added successfully!!"
    except Exception as error:
        return error

def GetPostById(id):
    result = PostModel.query.get(id)
    return result