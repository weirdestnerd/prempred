from datetime import datetime

from marshmallow import Schema, fields, post_load
from db.util import db_get


class Gameweek:
    def __init__(self, id=None, number=None, end_date:datetime=None):
        self.id = id
        self.number = number
        self.end_date = end_date

    def __repr__(self):
        return "<Gameweek(name={self.number!r})>".format(self=self)


class GameweekDB:
    @staticmethod
    def find(param):
        schema = GameweekSchema()
        gameweek = db_get('gameweeks', ['*'], param)
        return schema.dump(Gameweek(*gameweek))


class GameweekSchema(Schema):
    id = fields.Int(dump_only=True)
    number = fields.Int(required=True)
    end_date = fields.DateTime(required=True)

    @post_load
    def make_user(self, data, **kwargs):
        return Gameweek(**data)
