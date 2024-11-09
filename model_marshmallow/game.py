from datetime import datetime
from typing import Dict

from marshmallow import Schema, fields, post_load

from db.util import db_get
from service.schema.game_score.game_score import GameScoreSchema


class Game:
    def __init__(
            self,
            id=None,
            scores:Dict=None,
            started_at:datetime='',
            home_team_id:int=None,
            away_team_id:int=None,
            gameweek_id:int=None,
    ):
        self.id = id
        self.scores = scores
        self.started_at = started_at
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.gameweek_id = gameweek_id

    def __repr__(self):
        return "<Game(name={self.home_team!r})>".format(self=self)


class GameDB:
    @staticmethod
    def find(param):
        schema = GameSchema()
        game = db_get('games', ['*'], param)
        return schema.dump(Game(*game))


class GameSchema(Schema):
    id = fields.Int()
    scores = fields.Nested(GameScoreSchema())
    started_at = fields.DateTime()
    gameweek_id = fields.Int()
    home_team_id = fields.Int()
    away_team_id = fields.Int()

    @post_load
    def make_user(self, data, **kwargs):
        return Game(**data)