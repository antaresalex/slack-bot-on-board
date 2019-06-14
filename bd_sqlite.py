import time
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///schedule.sqlite')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    id_slack = Column(Integer, unique=True)
    position_type = Column(String(50))
    #start_date = Column()
    
    def __init__(self, first_name=None, last_name=None, id_slack=None, position_type=None):
        self.first_name = first_name
        self.last_name = last_name
        self.id_slack = id_slack
        self.position_type = position_type

    def __repr__(self):
        return '<User {} {}>'.format(self.first_name, self.last_name)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)