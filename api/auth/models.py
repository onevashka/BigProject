from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base


Base: DeclarativeMeta = declarative_base()

class AuthToken(Base):
    __tablename__ = 'auth_token'

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    email = Column(String, unique=True, index=True)

