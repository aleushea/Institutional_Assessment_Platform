from flask_sqlalchemy import SQLAlchemy
from os import path
from .db import db

DB_NAME = "database.db"

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .models import user, Exam
    create_database(app)

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')