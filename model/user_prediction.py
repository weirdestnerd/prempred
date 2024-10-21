from marshmallow import Schema, fields, post_load
from marshmallow.fields import Boolean

from db.util import db_get


class UserPrediction:
    def __init__(
            self,
            id=None,
            game_id:int=None,
            prediction_id:int=None,
            user_id:int=None,
            ai_suggested:Boolean=False,
    ):
        self.id = id
        self.game_id = game_id
        self.prediction_id = prediction_id
        self.user_id = user_id
        self.ai_suggested = ai_suggested

    def __repr__(self):
        return "<UserPrediction(game={self.game_id!r},user={self.user_id!r})>".format(self=self)


class UserPredictionDB:
    @staticmethod
    def find(param):
        schema = UserPredictionSchema()
        user_prediction = db_get('user_predictions', ['*'], param)
        return schema.dump(UserPrediction(*user_prediction))


class UserPredictionSchema(Schema):
    id = fields.Int()
    game_id = fields.Int()
    prediction_id = fields.Int()
    user_id = fields.Int()
    ai_suggested = fields.Boolean()

    @post_load
    def make_user(self, data, **kwargs):
        return UserPrediction(**data)