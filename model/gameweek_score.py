from marshmallow import Schema, fields, post_load

from db.util import db_get


class GameweekScore:
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
        return "<GameweekScore(gameweek={self.gameweek_id!r},user={self.user_id!r})>".format(self=self)


class GameweekScoreDB:
    @staticmethod
    def find(param):
        schema = GameweekScoreSchema()
        gameweek_score = db_get('gameweek_scores', ['*'], param)
        return schema.dump(GameweekScore(*gameweek_score))


class GameweekScoreSchema(Schema):
    id = fields.Int()
    gameweek_id = fields.Int()
    user_id = fields.Int()
    score = fields.Int()

    @post_load
    def make_user(self, data, **kwargs):
        return GameweekScore(**data)