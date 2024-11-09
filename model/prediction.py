from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import declarative_base

from model import Base


class Prediction(Base):
    __tablename__ = 'predictions'

    id = Column(Integer(), primary_key=True)
    name = Column(Text(), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"Prediction(id={self.id!r}, name={self.name!r})"
