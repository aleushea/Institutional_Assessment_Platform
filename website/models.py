from website import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from datetime import datetime

db = SQLAlchemy()
class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(10000))
    correct_ans = db.Column(db.String(150))
    stud_ans= db.Column(db.String(150))
    user_full_name = db.Column(db.String(50), db.ForeignKey('user.full_name'))
    # date = db.column(db.DateTime(timezone=True), default=func.now())
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.VARCHAR(50), unique=True)
    phone_number = db.Column(db.VARCHAR(20), unique=True)
    password = db.Column(db.VARCHAR(150))
    score = db.Column(db.Integer)
    feedback = db.Column(db.VARCHAR(150))
    exams = db.relationship('Exam')
    # date = db.column(db.DateTime(timezone=True), default=func.now())

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(200))
    choice1 = db.Column(db.String(100))
    choice2 = db.Column(db.String(100))
    choice3 = db.Column(db.String(100))
    choice4 = db.Column(db.String(100))
    correct_answer = db.Column(db.Integer)

    def __str__(self):
        return self.question_text