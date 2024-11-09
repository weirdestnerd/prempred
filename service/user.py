from typing import Tuple, Any

from sqlalchemy import select, column
from sqlalchemy.orm import Session

from db.util import get_db_engine
from model.user import User
from model_marshmallow.user import UserSchema


class UserService:
    @staticmethod
    def create_user(user):
        engine = get_db_engine()
        with Session(engine) as session:
            user = User(**user.__dict__)
            session.add(user)
            session.commit()

            return user


    @staticmethod
    def get_user(by: Tuple[str, Any]):
        engine = get_db_engine()
        schema = UserSchema()

        with Session(engine) as session:
            where_column = getattr(User, str(by[0]))
            query = select(User).where(where_column == by[1])
            return schema.dump(session.scalar(query))
