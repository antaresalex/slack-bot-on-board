from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=False)
    hiring_date = db.Column(db.DateTime, nullable=False)

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    send_days = db.Column(db.Integer, nullable=False)

#class Schedule(db.Model):
#    pass