from models import RelationshipModel
from models import db
from datetime import datetime, timezone


def AddRelation(id1,id2):

    try:
        relation = RelationshipModel()
        relation.user1_Id = id1
        relation.user2_Id = id2
        relation.status = 1 # Pending
        relation.action_by = id1

        db.session.add(relation)
        db.session.commit()

        return "relation added successfully!!"
    except Exception as error:
        db.session.rollback()
        return error

def GetRelation(id):
    result = ""
    return result