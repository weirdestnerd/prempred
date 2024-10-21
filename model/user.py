from marshmallow import Schema, fields, post_load
from db.util import db_insert, db_get

class User:
    def __init__(self, id=None, username='', acknowledge_ai=False):
        self.id = id
        self.username = username
        self.acknowledge_ai = acknowledge_ai

    def __repr__(self):
        return "<User(name={self.username!r})>".format(self=self)

class UserDB:
    @staticmethod
    def create(user):
        if not isinstance(user, User):
            return

        db_insert('users', user.__dict__.pop('id'))
        return UserDB.find(user.__dict__)

    @staticmethod
    def find(param):
        schema = UserSchema()
        user = db_get('users', ['*'], param)
        return schema.dump(User(*user))

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    acknowledge_ai = fields.Bool()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
