from flask  import Blueprint, render_template, request, flash, redirect, url_for
from .db import db
from .models import User, Exam
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, login_required, logout_user, current_user


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password1 = request.form.get('password')
        password2 = request.form.get('password2')
        
        errors = []
        
        # Check for existing user
        user_count = User.query.filter_by(email=email).count()
        if user_count > 0:
            errors.append('User already exists.')
        
        # Validate input
        if len(full_name) < 7:
            errors.append('Full name must be greater than 5 characters.')
        if len(email) < 5:
            errors.append('email must be at least 10 characters.')
        if password1 != password2:
            errors.append('Passwords don\'t match.')
        if len(password1) < 7:
            errors.append('Password must be at least 7 characters.')
        
        # If there are any errors, display them and return to the register page
        if errors:
            flash('\n'.join(errors), category='error')
            return render_template("register.html")
        
        # Create a new user
        new_user = User(full_name=full_name, email=email, password=generate_password_hash(password1, method='pbkdf2:sha256'))
        
        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(User, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))
        except IntegrityError:
            db.session.rollback()
            flash('User already exists.', category='error')
            return render_template("register.html")
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the account. Please try again.', category='error')
            return render_template("register.html")
    
    return render_template("register.html")
    
       

old file

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)        