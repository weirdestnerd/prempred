from marshmallow import Schema, fields, post_load
from marshmallow.fields import String

from db.util import db_get


class Prediction:
    def __init__(
            self,
            id=None,
            name:String='',
    ):
        self.id = id
        self.name = name

    def __repr__(self):
        return "<Prediction(name={self.name!r})>".format(self=self)


class PredictionDB:
    @staticmethod
    def find(param):
        schema = PredictionSchema()
        prediction = db_get('predictions', ['*'], param)
        return schema.dump(Prediction(*prediction))


class PredictionSchema(Schema):
    id = fields.Int()
    name = fields.Str()

    @post_load
    def make_user(self, data, **kwargs):
        return Prediction(**data)