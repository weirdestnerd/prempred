from marshmallow import Schema, fields, post_load

from db.util import db_get


class UserGameweekScore:
    def __init__(
            self,
            id=None,
            gameweek_id:int=None,
            user_id:int=None,
            score:int=0,
    ):
        self.id = id
        self.gameweek_id = gameweek_id
        self.user_id = user_id
        self.score = score

    def __repr__(self):
        return "<UserGameweekScore(gameweek={self.gameweek_id!r},user={self.user_id!r})>".format(self=self)


class UserGameweekScoreDB:
    @staticmethod
    def find(param):
        schema = UserGameweekScoreSchema()
        gameweek_score = db_get('user_gameweek_scores', ['*'], param)
        return schema.dump(UserGameweekScore(*gameweek_score))


class UserGameweekScoreSchema(Schema):
    id = fields.Int()
    gameweek_id = fields.Int()
    user_id = fields.Int()
    score = fields.Int()

    @post_load
    def make_user(self, data, **kwargs):
        return UserGameweekScore(**data)