"""
Flask application for spreadsheet-oriented formula generation and explanation.

This application allows users to input natural language descriptions and receive corresponding spreadsheet formulas.
It also provides explanations for given spreadsheet formulas. Users have daily limits for both formula generation and explanation.

The application includes the following components:
1. Flask routes for home, dashboard, user presence, formula generation, and explanation.
2. Decorator (`login_required`) for protecting routes that require user authentication.
3. Before request function (`check_user_existence`) to ensure the existence of the current user.
4. Background job using the APScheduler library to reset daily limits for all users.

Functions:
- `generate(user_input: str) -> Any`: Generates a spreadsheet formula from user input.
- `lecture(user_input: str) -> Any`: Explains a given spreadsheet formula.

Routes:
1. `/`: Application main route. Redirects to home if not authenticated, otherwise renders the main application page.
2. `/home`: Home route to display the landing page.
3. `/dashboard/`: Dashboard route to display user-specific information.
4. `/user`: Route to check user presence.

Note:
- User authentication is managed using the Flask `session` object.
- The application uses MongoDB for data storage.

Example Usage:
- Run the Flask application to start the server.
    a. gunicorn app:app
    b. flask --app app.py --debug run
- Access the application at the specified routes.

Make sure to set the required environment variables, such as SECRET_KEY and OPENAI_API_KEY, before running the application.
"""

import os
from datetime import timedelta
from functools import wraps

from flask import Flask, render_template, session, redirect, request, url_for, jsonify

from forsheets import generate, lecture
from user import db
from user.models import User

# start the database engine
db.start_db()

# Flask application initialization
app = Flask(__name__)
secret_key = os.getenv("SECRET_KEY")
app.secret_key = secret_key
app.permanent_session_lifetime = timedelta(minutes=30)


# Decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            curr_user = User.objects(email=session['user']['email']).first()
            if not curr_user:
                return redirect('/home')
            return f(*args, **kwargs)
        return redirect('/home')

    return wrap


@app.before_request
def check_user_existence():
    if request.endpoint == 'formula':
        if 'user' in session and 'email' in session['user']:
            user_email = session['user']['email']
            user = User.objects(email=user_email).first()

            if not user:
                # User is not found in the database, redirect to home
                return redirect(url_for('home'))


# routes
from user import routes


@app.route('/')
@login_required
def application():
    if session['logged_in'] is not True:
        return render_template('home.html')
    return render_template('app.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/dashboard/')
@login_required
def dashboard():
    user = User.objects(email=session['user']['email']).first()
    if user.history:
        return render_template('dashboard.html', user=user)
    return render_template('dashboard.html')


@app.get('/user')
def presence():
    if 'user' in session:
        user = User.objects(email=session['user']['email']).first()
        if user:
            data = {"session": session["logged_in"]}
        else:
            data = {"session": False}
        return jsonify(data)
    data = {"session": False}
    return jsonify(data)


@app.get('/formula')
def formula():
    reset_daily_limits()
    # Check formula_counter
    user = User.objects(email=session['user']['email']).first()
    if user.formula_counter <= 0:
        return jsonify("Daily formula limit reached. Upgrade for more!")

    user_input = request.args.get('user_input')
    if user_input == "":
        return "Please enter text"
    message = generate(user_input)

    # Update users' history
    if 'user' in session:
        user = User.objects(email=session['user']['email']).first()
        if user is None:
            return redirect('/user/signout')
        user.add_to_history(user_input, message[1:])
        user.formula_counter -= 1
        user.save()

    return message


@app.route('/explain', strict_slashes=False, methods=['GET'])
@login_required
def explain():
    # Check explanation_counter
    user = User.objects(email=session['user']['email']).first()
    if user.explanation_counter <= 0:
        return jsonify("Daily explanation limit reached. Upgrade for more!")

    user_input = request.args.get('user_input')
    if user_input == "Please enter text":
        return jsonify("This is your last warning")
    if user_input == "Daily formula limit reached. Upgrade for more!":
        return jsonify("Daily limit Reached")
    message = lecture(user_input)

    # Update counters in the database
    user.explanation_counter -= 1
    user.save()
    return message


""" reset users' access daily """


# Define a function to reset daily limits for all users
def reset_daily_limits():
    users = User.objects()
    for user in users:
        user.reset_daily_limits()
