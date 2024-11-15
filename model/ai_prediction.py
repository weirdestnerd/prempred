from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base

from model import Base


class AIPrediction(Base):
    __tablename__ = 'ai_predictions'

    id = Column(Integer(), primary_key=True)
    game_id = Column(Integer(), ForeignKey('games.id'))
    prediction_id = Column(Integer(), ForeignKey('predictions.id'))
    user_id = Column(Integer(), ForeignKey('users.id'))

    def __repr__(self) -> str:
        return f"AIPrediction(id={self.id!r})"
