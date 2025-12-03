from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column,Text,Integer,DateTime,ForeignKey,create_engine
from datetime import datetime

engine = create_engine("sqlite:///elegant.db", echo=True)   #converts sql to python and vice versa
Session = sessionmaker(bind=engine)  #allows interface with the database

def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()


Base = declarative_base()



class User(Base):

    __tablename__ = "users"

    id = Column(Integer,primary_key=True)
    username = Column(Text,nullable=False,unique=True)
    avatar_url = Column(Text, unique=True)
    bio = Column(Text) 

class Brand(Base):

    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now, nullable=False)


class Occasion (Base):

    __tablename__ = "occasions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, unique=True, nullable=False)
    description = Column(Text)


class Outfit(Base):

    __tablename__ = "outfits"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    occasion_id = Column(Integer, ForeignKey("occasions.id"))

    name = Column(Text, nullable=False)
    description = Column(Text)
    color = Column(Text)
    image_url = Column(Text)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
