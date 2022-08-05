from sqlalchemy import Column, Integer, String, Boolean, DATETIME
from db import Base, ENGINE

class record_table(Base):
    __tablename__ = 'record_table'
    id = Column(Integer,primary_key=True,autoincrement=True)
    dt = Column(DATETIME)
    file_address = Column(String(150),nullable=False)
    ticket = Column(String(30),nullable=False)
    finished = Column(Boolean,default=False)
    result = Column(String(4000),nullable=True)

class record_table_temp(Base):
    __tablename__ = 'record_table_temp'
    id = Column(Integer,primary_key=True,autoincrement=True)
    file_address = Column(String(150),nullable=False)
    ticket = Column(String(30),nullable=False)
    result = Column(String(4000),nullable=True)

def create_table():
    Base.metadata.create_all(bind=ENGINE)
