from datetime import date
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///bot_db.sqlite')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    slack_id = Column(String(50), unique=True) 
    position_type = Column(Integer, unique=True)
    start_date = Column(Date)
    
    def __init__(self, first_name=None, last_name=None, id_slack=None, position_type=None, start_date=None):
        self.first_name = first_name
        self.last_name = last_name
        self.slack_id = slack_id
        self.position_type = position_type
        self.start_date = start_date

    def __repr__(self):
        return '<User {} {} {}>'.format(self.first_name, self.last_name, self.position_type)

class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    text = Column(String(600))
    interval = Column(Integer)

    def __init__(self, text=None, interval=None):
        self.text = text
        self.interval = interval

    def __repr__(self):
        return '<Event {} {}>'.format(self.text, self.interval)

class Position_type(Base):
    __tablename__ = 'position_type'
    id = Column(Integer, primary_key=True)
    position_name = Column(String(50))
    
    def __init__(self, position_name=None):
        self.position_name = position_name

    def __repr__(self):
        return '<Position type {}>'.format(self.position_name)

class Position_event(Base):
    __tablename__ = 'position_event'
    id = Column(Integer, primary_key=True)
    position_type = Column(Integer, unique=True)
    event = Column(Integer, unique=True)
    
    def __init__(self, position_type=None, event=None):
        self.position_type = position_type
        self.event = event
        
    def __repr__(self):
        return '<Position event {} {}>'.format(self.position_type, self.event)

class Schudule(Base):
    __tablename__ = 'schudule'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    position_event = Column(Integer, unique=True)
    delivery_date = Column(Date)
    delivery_status = Column(String(50))
    
    def __init__(self, user_id=None, position_event=None, delivery_date=None, delivery_status=None):
        self.user_id = user_id
        self.position_event = position_event
        self.delivery_date = delivery_date
        self.delivery_status = delivery_status
        
    def __repr__(self):
        return '<Schedule {} {} {}>'.format(self.position_event, self.delivery_date, self.delivery_status)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)