import os
import datetime

import jwt
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from model import Base


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer(), primary_key=True)
    username = Column(String(150), nullable=False, unique=True)
    acknowledge_ai = Column(Boolean(), default=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    registered_on = Column(DateTime, nullable=False)
    admin = Column(Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        pass
        # self.email = email
        # self.password = bcrypt.generate_password_hash(
        #     password, app.config.get('BCRYPT_LOG_ROUNDS')
        # ).decode()
        # self.registered_on = datetime.datetime.now()
        # self.admin = admin


    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"


    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=10),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                os.getenv('AUTH_TOKEN_GEN_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e


    def encode_refresh_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                os.getenv('AUTH_TOKEN_GEN_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e


    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, os.getenv('AUTH_TOKEN_GEN_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            print('Signature expired. Please log in again.')
            return None
        except jwt.InvalidTokenError:
            print('Invalid token. Please log in again.')
            return None

