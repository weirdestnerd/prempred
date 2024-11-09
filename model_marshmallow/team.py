from marshmallow import Schema, fields, post_load
from db.util import db_get


class Team:
    def __init__(self, id=None, full_name='', short_name='', acronym='', color=''):
        self.id = id
        self.full_name = full_name
        self.short_name = short_name
        self.acronym = acronym
        self.color = color

    def __repr__(self):
        return "<Team(name={self.full_name!r})>".format(self=self)


class TeamDB:
    @staticmethod
    def find(param):
        schema = TeamSchema()
        team = db_get('teams', ['*'], param)
        return schema.dump(Team(*team))


class TeamSchema(Schema):
    id = fields.Int(dump_only=True)
    full_name = fields.Str(required=True)
    short_name = fields.Str(required=True)
    acronym = fields.Str()
    color = fields.Str()

    @post_load
    def make_user(self, data, **kwargs):
        return Team(**data)
