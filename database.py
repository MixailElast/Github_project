from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from databases import Database

DATABASE_URL = "sqlite:///./test.db"

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
Base = declarative_base()


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    views = Column(Integer, default=0)
    cooking_time = Column(Integer)
    ingredients = Column(Text)
    description = Column(Text)


Base.metadata.create_all(bind=engine)
