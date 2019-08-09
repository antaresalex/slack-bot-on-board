from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    slack_id = db.Column(db.String, nullable=False, unique=True)
    position_type = db.Column(db.Integer,
                              db.ForeignKey('position_type.id'),
                              nullable=False)
    start_date = db.Column(db.Date, nullable=False)

    # Связь с таблицей position_type.
    # Позволяет вызвать всех пользователей должности Position_type.employees
    position = db.relationship('Position_type',
                               backref=db.backref('employees', lazy='dynamic'))

    def __repr__(self):
        return '<Employee {} {} {}>'.format(self.first_name,
                                            self.last_name,
                                            self.start_date)


# Дополнительная таблица для связи event и position_type
position_event = db.Table('position_event',
                          db.Column('position_type',
                                    db.Integer,
                                    db.ForeignKey('position_type.id')),
                          db.Column('event',
                                    db.Integer,
                                    db.ForeignKey('event.id')))


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String, nullable=False)
    html_text = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=True)
    interval = db.Column(db.Integer, nullable=False)

    # Связь с многие-ко-многим таблицы event и position_type
    positions = db.relationship('Position_type',
                                secondary=position_event,
                                backref=db.backref('events', lazy='dynamic'))

    def __repr__(self):
        return '<Event {} {}>'.format(self.text, self.interval)


class Position_type(db.Model):
    __tablename__ = 'position_type'
    id = db.Column(db.Integer, primary_key=True)
    position_name = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return '<Position type {}>'.format(self.position_name)


class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    delivery_date = db.Column(db.DateTime, nullable=False)
    delivery_status = db.Column(db.String, nullable=True)

    # Связь с таблицей Employee. Позволяет вызвать все расписание для пользователя
    # Employee.shedules
    employee = db.relationship('Employee',
                               backref=db.backref('schedules',
                                                  cascade="all, delete-orphan",
                                                  lazy='dynamic'))

    # Связь с таблицей event. Позволяет вызвать все расписания
    # связанные с событием Event.shedules
    event = db.relationship('Event',
                            backref=db.backref('schedules',
                                               cascade="all, delete-orphan",
                                               lazy='dynamic'))

    def __repr__(self):
        return '<Schedule {} {} {}>'.format(self.employee_id,
                                            self.delivery_date,
                                            self.delivery_status)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(128))
    role = db.Column(db.Integer,
                     db.ForeignKey('role.id'),
                     nullable=False)

    role_type = db.relationship('Role',
                                backref=db.backref('users', lazy='dynamic'))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role_type.name == 'admin'

    def __repr__(self):
        return '<User {} {}>'.format(self.first_name,
                                     self.username)


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return '<User role {}>'.format(self.name)
