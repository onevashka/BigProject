from sqlalchemy import Column, Integer, String, Boolean
from db import Base 


class Task(Base):

    __tablename__ = "Task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tittle = Column(String, nullable=False)
    Is_acctive = Column(Boolean, default=True)