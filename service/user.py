from models import User
from models import db
from datetime import datetime, timezone
import errors

def AddUser(name,email):

    try:
        user = User()
        #user.id = id
        user.name = name
        user.email = email
        user.password = '1'

        db.session.add(user)
        db.session.commit()

        return "User added successfully!!"
    except Exception as error:
        return errors.internal_error(error)

def GetUserById(id):
    result = User.query.get(id)
    return result

def GetAllUsers():
    restult = User.query.all()
    return restult

def Search(text):
    #result = db.session.query(User).filter(User.name =="jalal")
    if text:
        result = db.session.query(User).filter(User.name.like('%'+text+'%'))
        return result
    else:
        return ""