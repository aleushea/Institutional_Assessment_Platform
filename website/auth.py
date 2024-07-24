from flask  import Blueprint, render_template, request, flash, redirect, url_for
# from .db import db
from .models import User, db, Question
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
    
        user = User.query.filter_by(phone_number=phone_number).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in sucessfully!', category='success')
                # login_user(User, remember=True)
                return redirect(url_for('auth.Examination'))                      
            else:
                flash('Incorrect Password.try again.', category='error')
        else:
            flash('The user doesnt exist please create an acoount', category='error')

    return render_template("login.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        phone_number = request.form.get('phone_number')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        errors = []
        
        # Check for existing user
        user_count = User.query.filter_by(phone_number=phone_number).count()
        if user_count > 0:
            errors.append('User already exists.')
        
        # Validate input
        if len(full_name) < 5:
            errors.append('Full name must be greater than 5 characters.')
        if len(phone_number) < 9:
            errors.append('Phone number must be at least 10 characters.')
        if password1 != password2:
            errors.append('Passwords don\'t match.')
        if len(password1) < 7:
            errors.append('Password must be at least 7 characters.')
        
        # If there are any errors, display them and return to the sign-up page
        if errors:
            flash('\n'.join(errors), category='error')
            return render_template("sign_up.html")
        
        # Create a new user
        new_user = User(full_name=full_name, phone_number=phone_number, password=generate_password_hash(password1, method='pbkdf2:sha256'))
        
        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(User, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))
        except IntegrityError:
            db.session.rollback()
            flash('User already exists.', category='error')
            return render_template("sign_up.html")
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the account. Please try again.', category='error')
            return render_template("sign_up.html")
    
    return render_template("sign_up.html")

@auth.route('/insert_question', methods=['POST'])
def insert_question():
    if request.method == 'POST':
        question_text = request.form['question']
        choice1 = request.form['choice1']
        choice2 = request.form['choice2']
        choice3 = request.form['choice3']
        choice4 = request.form['choice4']
        correct_answer = int(request.form['answer'])

        new_question = Question(question_text=question_text, choice1=choice1, choice2=choice2, choice3=choice3, choice4=choice4, correct_answer=correct_answer)
        db.session.add(new_question)
        db.session.commit()

        return "Question inserted successfully!"

@auth.route('/Examination', methods=['GET', 'POST'])
def Examination():
    questions = Question.query.all()
    return render_template('Examination.html', questions=questions)
