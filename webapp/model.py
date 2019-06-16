from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    slack_id = db.Column(db.String, nullable=False, unique=True)
    position_type = db.Column(db.String, nullable=False) # FK Как сделать?
    start_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<User {} {} {}>'.format(self.first_name, self.last_name, self.start_date)

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    interval = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Event {} {}>'.format(self.text, self.interval)

class Position_type(db.Model):
    __tablename__ = 'position_type'
    id = db.Column(db.Integer, primary_key=True)
    position_name = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return '<Position type {}>'.format(self.position_name)

class Position_event(db.Model):
    __tablename__ = 'position_event'
    id = db.Column(db.Integer, primary_key=True)
    position_type = db.Column(db.Integer, nullable=False)
    event = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Position and event {} {}>'.format(self.position_type, self.event)

class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    event = db.Column(db.Integer, nullable=False)
    delivery_date = db.Column(db.DateTime, nullable=False)
    delivery_status = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<Schedule {} {} {}>'.format(self.user_id, self.delivery_date, self.delivery_status)


    