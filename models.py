from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()  

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }


class User(BaseModel, db.Model):
    """Model for the users table"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(128), index=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    modified_at = db.Column(db.DateTime)
    #relationships = db.relationship('RelationshipModel', lazy='dynamic')

class Post(BaseModel, db.Model):
    """Model for the posts table"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True) 
    text = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    image_id = db.Column(db.Integer(), nullable=True)
    created_at = db.Column(db.DateTime,index=True, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime)
    likes = db.Column(db.Integer(), nullable=False,default = 0)

class Relationship(BaseModel, db.Model):
    """Model for the relationships table"""
    __tablename__ = 'relationships'
    __table_args__ = (
        db.UniqueConstraint('user1_Id', 'user2_Id', name='unique_user1_Id_user2_Id'),
    )
    id = db.Column(db.Integer, primary_key=True) 
    user1_Id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user2_Id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.Integer,nullable=False,default=0)
    # 0 : not friends , 1: Pending, 2: Friends, 3:declined
    action_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime,index=True, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime)
