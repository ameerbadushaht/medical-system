from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import backref




class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    age = db.Column(db.Integer)
    address = db.Column(db.String(150))
    phone = db.Column(db.Integer)
    bg= db.Column(db.String(150))
    relative = db.Column(db.String(150))
    gender= db.Column(db.String(150))
    notes = db.relationship('Note')
    doctor_id= db.Column(db.Integer, db.ForeignKey("doctor.id"))
    def get_id(self):
           return (self.user_id)


class Doctor(db.Model,UserMixin):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150),  unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    phone = db.Column(db.Integer)
    user=db.relationship('User',uselist=False,backref=db.backref('doctor',uselist=False))

