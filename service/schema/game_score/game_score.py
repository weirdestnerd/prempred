from marshmallow import Schema, fields, post_load

class GameScore:
    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team

class GameScoreSchema(Schema):
    home_team = fields.Int(required=True)
    away_team = fields.Int(required=True)

    @post_load
    def make_user(self, data, **kwargs):
        return GameScore(**data)