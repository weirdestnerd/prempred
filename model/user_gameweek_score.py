from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base

from model import Base


class UserGameweekScore(Base):
    __tablename__ = 'user_gameweek_scores'

    id = Column(Integer(), primary_key=True)
    gameweek_id = Column(Integer(), ForeignKey('gameweeks.id'))
    user_id = Column(Integer(), ForeignKey('users.id'))
    score = Column(Integer(), default=0)

    def __repr__(self) -> str:
        return f"UserGameweekScore(id={self.id!r})"
