from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import declarative_base, relationship

from model import Base


class Gameweek(Base):
    __tablename__ = 'gameweeks'

    id = Column(Integer(), primary_key=True)
    number = Column(Integer(), nullable=False, unique=True)
    end_date = Column(DateTime())

    def __repr__(self) -> str:
        return f"Gameweek(number={self.number!r}, end_date={self.end_date!r})"
