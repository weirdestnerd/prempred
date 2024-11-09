from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.util import get_db_engine
from model.gameweek import Gameweek
from model_marshmallow.gameweek import GameweekSchema
from service.game import GameService
from service.schema.gameweek.with_games import GameweekWithGamesSchema, GameweekWithGames


class GameweekService:
    def __init__(self):
        super().__init__()


    def current_gw(self):
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

        engine = get_db_engine()
        with Session(engine) as session:
            query = select(Gameweek).where(Gameweek.end_date >= datetime.now())
            return self.__load_gameweek(session.scalar(query))


    def __load_gameweek(self, gameweek):
        games = GameService().gw_games(gameweek=gameweek)
        gameweek = GameweekWithGames(*GameweekSchema().dump(gameweek), games=games)
        return GameweekWithGamesSchema().dump(gameweek)
