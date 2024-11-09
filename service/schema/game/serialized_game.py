from datetime import datetime
from typing import Dict

from marshmallow import fields, post_load
from marshmallow.fields import String

from model_marshmallow.game import Game, GameSchema
from model_marshmallow.gameweek import Gameweek, GameweekSchema
from model_marshmallow.team import Team, TeamSchema


class SerializedGame(Game):
    def __init__(
            self,
            id=None,
            scores: Dict = None,
            started_at: datetime = '',
            home_team: Team = None,
            away_team: Team = None,
            gameweek: Gameweek = None,
            user_prediction : String = '',
            ai_prediction : String = '',
    ):
        super().__init__(id, scores, started_at)
        self.home_team = home_team
        self.away_team = away_team
        self.gameweek = gameweek
        self.user_prediction = user_prediction
        self.ai_prediction = ai_prediction

class SerializedGameSchema(GameSchema):
    home_team = fields.Nested(TeamSchema())
    away_team = fields.Nested(TeamSchema())
    gameweek = fields.Nested(GameweekSchema(only=["number"]))
    user_prediction = fields.String()
    ai_prediction = fields.String()

    @post_load
    def make(self, data, **kwargs):
        return SerializedGame(**data)
