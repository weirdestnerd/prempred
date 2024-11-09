from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

from model import Base


class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer(), primary_key=True)
    full_name = Column(String(), nullable=False, unique=True)
    short_name = Column(String(), nullable=False)
    acronym = Column(String())
    color = Column(String())

    def __repr__(self) -> str:
        return f"Team(id={self.id!r}, username={self.username!r})"
