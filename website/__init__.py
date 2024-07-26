from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
import os
from .models import db
from .question import question_bp  # Import your question blueprint
from .take_exam import take_Exam
from .exam_Page import *
from .Add_question import *


def create_app():
    app = Flask(__name__)
    app.template_folder = 'template'
    app.static_folder = 'static'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/institutional_assessment_platform'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///institutional_assessment_platform.db'
    app.config['SECRET_KEY'] = '1212'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        # print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        db.create_all()

    from .views import views as views_blueprint
    app.register_blueprint(views_blueprint, url_prefix='/')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/')

    # Register the question blueprint with insert, update, and delete routes
    app.register_blueprint(question_bp)

    app.register_blueprint(take_Exam)
    
    app.register_blueprint(exam_page_bp)
    app.register_blueprint(Add_question_bp)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        from .models import User
        return User.query.get(int(id))

    return app