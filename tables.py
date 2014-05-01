from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///nodes.db')
Base = declarative_base()

class Nodes(Base):
    __tablename__ = 'nodes'

    nodeID = Column(Integer, primary_key=True)
    hostname = Column(String, unique=True)
    key = Column(String, unique=True)
    mac = Column(String, unique=True)
    nickname = Column(String)
    email = Column(String)
    coords = Column(String)
    token = Column(String)

# create tables
Base.metadata.create_all(engine)
