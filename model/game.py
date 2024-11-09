from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base

from model import Base


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer(), primary_key=True)
    scores = Column(JSONB(), nullable=False)
    started_at = Column(DateTime(), nullable=False)
    home_team_id = Column(Integer(), ForeignKey('teams.id'))
    away_team_id = Column(Integer(), ForeignKey('teams.id'))
    gameweek_id = Column(Integer(), ForeignKey('gameweeks.id'))

    def __repr__(self) -> str:
        return f"Game(id={self.id!r})"
