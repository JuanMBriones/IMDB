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
from connector import DatabaseConnector

Base = declarative_base(
    metadata=MetaData(),
)

data_connector = DatabaseConnector()

engine = create_engine(
    data_connector.get_postgres_uri(),
    isolation_level="REPEATABLE READ",
)


class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True)
    preference_key = Column(Integer)
    movie_title = Column(String)
    rating = Column(Float)
    year = Column(Integer)
    create_time = Column(TIMESTAMP(timezone=True), index=True)


def start_mappers():
    Base.metadata.create_all(engine)