from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///nodes.db')
Base = declarative_base()

class Nodes(Base):
    __tablename__ = 'nodes'

    nodeID = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    fastdkey = Column(String, unique=True)
    mac = Column(String, unique=True)
    nick = Column(String)
    email = Column(String)
    coord = Column(String)

