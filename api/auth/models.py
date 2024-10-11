from sqlalchemy import Column, String, Boolean, Table, Integer
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta


Base: DeclarativeMeta = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    disabled = Column(Boolean, default=None)




