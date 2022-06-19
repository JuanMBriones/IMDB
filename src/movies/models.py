import os
from sqlalchemy import (
    MetaData,
    Column,
    Integer,
    String,
    Float,
    TIMESTAMP,
    Text,
    create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from connector import DatabaseConnector
from sqlalchemy.orm import sessionmaker
from flask_login import UserMixin

data_connector = DatabaseConnector()

Base = declarative_base(
    metadata=MetaData(),
)
engine = create_engine(
    data_connector.get_postgres_uri(),
    isolation_level="REPEATABLE READ",
)

Session = sessionmaker(bind = engine)
session = Session()


class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True)
    preference_key = Column(Integer)
    movie_title = Column(String)
    rating = Column(Float)
    year = Column(Integer)
    create_time = Column(TIMESTAMP(timezone=True), index=True)


class User(UserMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = Column(String(100), unique=True)
    password = Column(String(100))
    name = Column(String(1000))
    preference_key = Column(Integer)


def start_mappers():
    Base.metadata.create_all(engine)