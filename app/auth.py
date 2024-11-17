from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from app.models import User, db  # Ensure your models are correctly imported

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if user exists and validate password
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):  # Validate hashed password
            login_user(user)  # Log the user in using Flask-Login
            return redirect(url_for('home'))  # Redirect to home or dashboard
        else:
            flash("Invalid credentials. Please try again.", "danger")

    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validation checks
        if not username or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for('auth.register'))

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash("Username already taken. Please choose a different one.", "danger")
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash("Email is already registered.", "danger")
            return redirect(url_for('auth.register'))

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        # Create a new user object
        new_user = User(username=username, email=email, password=hashed_password)

        # Add the new user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for('auth.login'))  # Redirect to login after registration
        except Exception as e:
            db.session.rollback()  # Rollback if there is an error
            flash("There was an issue creating your account. Please try again.", "danger")
            return redirect(url_for('auth.register'))

    return render_template('register.html')
