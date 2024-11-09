from datetime import datetime

from marshmallow import Schema, fields, post_load

from model_marshmallow.gameweek import Gameweek
from service.schema.game.serialized_game import SerializedGameSchema, SerializedGame


class GameweekWithGames(Gameweek):
    def __init__(self, id=None, number=None, end_date:datetime=None, games:list[SerializedGame]=[]):
        super().__init__(id, number, end_date)
        self.games = games

class GameweekWithGamesSchema(Schema):
    id = fields.Int(dump_only=True)
    number = fields.Int(required=True)
    games = fields.List(fields.Nested(SerializedGameSchema()))

    @post_load
    def make_user(self, data, **kwargs):
        return GameweekWithGames(**data)