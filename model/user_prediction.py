from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base

from model import Base


class UserPrediction(Base):
    __tablename__ = 'user_predictions'

    id = Column(Integer(), primary_key=True)
    game_id = Column(Integer(), ForeignKey('games.id'))
    prediction_id = Column(Integer(), ForeignKey('predictions.id'))
    user_id = Column(Integer(), ForeignKey('users.id'))
    ai_suggested = Column(Boolean(), default=False)

    def __repr__(self) -> str:
        return f"UserPrediction(id={self.id!r})"
