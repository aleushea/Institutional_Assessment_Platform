from json import JSONEncoder
from flask  import Blueprint, render_template, request, flash, redirect, url_for
from .db import db
from .models import User, db, Question
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    role = request.args.get('role')  # Extract the role parameter from the URL
    
    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        
        user = User.query.filter_by(phone_number=phone_number).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                if user.role == 'student':
                    return redirect(url_for('auth.Examination'))
                elif user.role == 'teacher':
                    return redirect(url_for('auth.manage_questions'))
                elif user.role == 'sys_admin':
                    return redirect(url_for('auth.manage_users'))
            else:
                flash('Incorrect Password. Try again.', category='error')
        else:
            flash('The user does not exist. Please create an account.', category='error')
    
    if role == 'student':
        return render_template('login_as_student.html')
    elif role == 'teacher':
        return render_template('login_as_teacher.html')
    elif role == 'sys_admin':
        return render_template('login_as_admin.html')
    else:
        return "Invalid role selected"
    
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
        role = request.form.get('role') 
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
        new_user = User(full_name=full_name, role=role, phone_number=phone_number, password=generate_password_hash(password1, method='pbkdf2:sha256'))
        
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
            return render_template("login.html")
    
    return render_template("sign_up.html")

@auth.route('/student_login')
def student_login():
    return render_template('student_login.html', role='student')

@auth.route('/login_as_teacher')
def login_as_teacher():
    return render_template('login_as_teacher.html', role='teacher')

@auth.route('/login_as_admin')
def login_as_admin():
    return render_template('login_as_admin.html', role='sys_admin')

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Question):
            return obj.__dict__
        return super().default(obj)


@auth.route('/Examination', methods=['GET', 'POST'])
def Examination():
    first_question = Question.query.first()
    
    if first_question:
        question_data = {
            'id': first_question.id,
            'question_text': first_question.question_text,
            'choice1': first_question.choice1,
            'choice2': first_question.choice2,
            'choice3': first_question.choice3,
            'choice4': first_question.choice4
        }
        return render_template('exam_question.html', question=question_data)
    else:
        # Handle the case where there are no questions in the database
        no_question_message = "There are currently no questions in the database."
        return render_template('no_questions_message.html', message=no_question_message)
    
@auth.route('/submit_answer', methods=['POST'])
def submit_answer():
    if request.method == 'POST':
        question_id = request.form.get('question_id')
        answer = request.form.get('answer')
        # Process the submitted answer here
        return f"Question ID: {question_id}, Answer: {answer}"
    return "Invalid request"

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
    else:
        return "Method Not Allowed", 405  # Return a 405 status code for methods other than POST

@auth.route('/exam_question', methods=['GET', 'POST'])
def display_exam_question():
    que = Question.query.all()  # Retrieve the first question from the database for demonstration
    return render_template('exam_question.html', question_text=que.question_text, choice1=que.choice1, choice2=que.choice2, choice3=que.choice3, choice4=que.choice4)

@auth.route('/manage_questions', methods=['GET', 'POST'])
def manage_questions():
    # Add authentication check here to ensure only teachers can access this route
    if request.method == 'GET':
        questions = Question.query.all()  # Retrieve all questions from the database
        return render_template('manage_questions.html', questions=questions)
    
    elif request.method == 'POST':
        # Add, edit, or delete functionality for questions here
        # Example code to add a new question:
        new_question = Question(question_text='question_text', choice1='Choice 1', choice2='Choice 2', choice3='Choice 3', choice4='Choice 4')
        db.session.add(new_question)
        db.session.commit()
        
        flash('New question added successfully!', category='success')
        return redirect(url_for('auth.manage_questions'))
    
@auth.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    # Add authentication check here to ensure only sys_admin can access this route
    
    if request.method == 'GET':
        users = User.query.all()  # Retrieve all users from the database
        return render_template('manage_users.html', users=users)
    
    elif request.method == 'POST':
        # Add functionality to give rights to users here
        # Example code to grant admin rights to a user:
        user_id = request.form.get('user_id')
        user = User.query.get(user_id)
        user.is_admin = True
        db.session.commit()
        
        flash('Admin rights granted to the user successfully!', category='success')
        return redirect(url_for('auth.manage_users'))


@auth.route('/schedule_exam', methods=['GET', 'POST'])
def schedule_exam():
    # Add authentication check here to ensure only sys_admin can access this route
    
    if request.method == 'GET':
        # Render the schedule exam form
        return render_template('schedule_exam.html')
    
    elif request.method == 'POST':
        # Add functionality to schedule exams here
        # Example code to schedule an exam:
        exam_date = request.form.get('exam_date')
        exam_subject = request.form.get('exam_subject')
        
        # Code to schedule the exam in the database
        
        flash('Exam scheduled successfully!', category='success')
        return redirect(url_for('auth.schedule_exam'))