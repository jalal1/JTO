from models import Relationship, User
from models import db
from datetime import datetime, timezone
from flask import render_template
import errors
from sqlalchemy import or_
from sqlalchemy.sql import union, select


def UpdateRelation(id1, id2, status, action_by):

    try:
        relation = Relationship()
        if id1 < id2:
            relation.user1_Id = id1
            relation.user2_Id = id2
        else:
            relation.user1_Id = id2
            relation.user2_Id = id1

        relation.status = status
        relation.action_by = action_by

        db.session.add(relation)
        db.session.commit()

        return "relation added successfully!!"
    except Exception as error:
        return errors.internal_error(error)


def GetRelation(id):
    result = ""
    return result


def GetFriends(id):
    q1 = db.session.query(User).join(
        Relationship, User.id == Relationship.user1_Id).filter(Relationship.user2_Id == id, Relationship.status==2)
    q2 = db.session.query(User).join(
        Relationship, User.id == Relationship.user2_Id).filter(Relationship.user1_Id == id, Relationship.status==2)
    result = q1.union(q2)

    return result
##
def GetAll(id):
    q1 = db.session.query(User).add_columns(User.id,User.name,Relationship.status).join(
        Relationship, User.id == Relationship.user1_Id).filter(Relationship.user2_Id == id)
    q2 = db.session.query(User).add_columns(User.id,User.name,Relationship.status).join(
        Relationship, User.id == Relationship.user2_Id).filter(Relationship.user1_Id == id)
    #q3 = db.session.query(User).add_columns(User.id,User.name,'null').filter(User.id != id)
    result = q1.union(q2)

    return result