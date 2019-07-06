from models import UserModel
from models import db
from datetime import datetime, timezone


def AddUser(email):

    try:
        user = UserModel()
        #user.id = id
        user.name = 'Jalal'
        user.email = email
        user.password = '1'
        user.created_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")

        db.session.add(user)
        db.session.commit()

        return "User added successfully!!"
    except Exception as error:
        return error

def GetUserById(id):
    result = UserModel.query.get(id)
    return result