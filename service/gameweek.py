from service.schema.gameweek.with_games import GameweekWithGamesSchema
from marshmallow import INCLUDE

class GameweekService:
    def __init__(self):
        super()

    def current_gw(self):
        # TODO: base on current time, get current gameweek
        #   current_time <= gameweek.end_date
        dummy = {
            'id': '1',
            'number': '8',
            'end_date': '2024-10-10T15:00:00.000Z',
            'games': [{
                'id': '1',
                'gameweek': {
                    'number': '8',
                },
                'started_at': '2024-10-10T15:00:00.000Z',
                'scores': {
                    'home_team': '3',
                    'away_team': '2',
                },
                'home_team': {
                    'full_name': 'arsenal',
                    'short_name': 'arsenal',
                    'acronym': 'ars',
                    'color': 'red',
                },
                'away_team': {
                    'full_name': 'chelsea',
                    'short_name': 'chelsea',
                    'acronym': 'che',
                    'color': 'blue',
                },
                'user_prediction': 'chelsea',
                'ai_prediction': '',
            }],
        }

        # TODO: db.get gameweek, dg.gets games w/ user & ai predictions
        #   GameweekWithGames(*gameweek, games=games)
        schema = GameweekWithGamesSchema()
        gameweek = schema.load(dummy, unknown=INCLUDE)
        return schema.dump(gameweek)
