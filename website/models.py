from flask_login import UserMixin
from .db import db
from sqlalchemy.sql import func 
class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(10000))
    correct_ans = db.Column(db.String(150))
    stud_ans= db.Column(db.String(150))
    user_full_name = db.Column(db.String(50), db.ForeignKey('user.full_name'))
    # date = db.column(db.DateTime(timezone=True), default=func.now())
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), unique=True)
    phone_number = db.Column(db.Integer, unique=True)
    password = db.Column(db.String(150))
    score = db.Column(db.Integer)
    feedback = db.Column(db.String(150))
    exams = db.relationship('Exam')
