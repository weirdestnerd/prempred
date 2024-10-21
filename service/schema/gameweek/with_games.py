from datetime import datetime

from model.game import Game
from model.gameweek import Gameweek
from marshmallow import Schema, fields, post_load

from service.schema.game.serialized_game import SerializedGameSchema


class GameweekWithGames(Gameweek):
    def __init__(self, id=None, number=None, end_date:datetime=None, games:list[Game]=[]):
        super().__init__(id, number, end_date)
        self.games = games

class GameweekWithGamesSchema(Schema):
    id = fields.Int(dump_only=True)
    number = fields.Int(required=True)
    games = fields.List(fields.Nested(SerializedGameSchema()))

    @post_load
    def make_user(self, data, **kwargs):
        return GameweekWithGames(**data)