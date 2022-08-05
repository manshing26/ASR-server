import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

user_name = os.environ['MYSQL_USER']
password = os.environ['MYSQL_PASSWORD']
database_name = os.environ['MYSQL_DATABASE']
host = "db"

DATABASE = 'mysql://%s:%s@%s/%s?charset=utf8' % (
    user_name,
    password,
    host,
    database_name,
)

# create engine
ENGINE = create_engine(
    DATABASE,
    encoding="utf-8",
    echo=False,
    pool_pre_ping=True, # Mysql will go away after 8 hours idle time
)

Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=ENGINE
)

Base = declarative_base()

def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

Base.to_dict = to_dict