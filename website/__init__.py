from flask import Flask
from .database import init_db
from .db import db
from .models import User, Exam
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.template_folder = 'template'
    app.static_folder = 'static'
    app.config['SECRET_KEY'] = 'Alex'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app)

    with app.app_context():
        db.create_all()

    from .views import views as views_blueprint
    app.register_blueprint(views_blueprint, url_prefix='/')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/')
      
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app
