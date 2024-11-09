from flask import session
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.util import get_db_engine
from model.ai_prediction import AIPrediction
from model.game import Game
from model.team import Team
from model.user_prediction import UserPrediction
from model_marshmallow.ai_prediction import AIPredictionSchema
from model_marshmallow.gameweek import Gameweek, GameweekSchema
from model_marshmallow.team import TeamSchema
from model_marshmallow.user_prediction import UserPredictionSchema
from service.schema.game.serialized_game import SerializedGame, SerializedGameSchema
from service.user import UserService


class GameService:
    def __init__(self):
        super().__init__()


    def gw_games(self, gameweek:Gameweek=None):
        if gameweek is None:
            return []

        engine = get_db_engine()
        with Session(engine) as session:
            query = select(Game).filter_by(gameweek_id = gameweek.id)
            games = session.scalars(query)

        return map(self.__load_game, games)


    def __load_game(self, game):
        user = UserService.get_user('olu') # TODO: use current_user
        engine = get_db_engine()
        with Session(engine) as session:
            query = select(UserPrediction).where(UserPrediction.user_id == user.id).where(UserPrediction.game_id == game.id)
            user_prediction = UserPredictionSchema().dump(session.scalar(query))

            query = select(AIPrediction).where(AIPrediction.user_id == user.id).where(AIPrediction.game_id == game.id)
            ai_prediction = AIPredictionSchema().dump(session.scalar(query))

            loaded_game = {
                **game,
                'home_team': TeamSchema().dump(session.get(Team, game.home_team_id)),
                'away_team': TeamSchema().dump(session.get(Team, game.away_team_id)),
                'gameweek': GameweekSchema().dump(session.get(Gameweek, game.gameweek_id)),
                user_prediction: user_prediction.name,
                ai_prediction: ai_prediction.name,
            }

        return self.__serialize_game(loaded_game)


    def __serialize_game(self, game):
        schema = SerializedGameSchema()
        return schema.dump(SerializedGame(*game))
