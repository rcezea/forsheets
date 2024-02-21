import os
from datetime import timedelta
from functools import wraps

from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask, render_template, session, redirect, request, url_for, jsonify
from flask_apscheduler import APScheduler

from formulai import generate, lecture
from user import db
from user.models import User

# start the database engine
db.start_db()

# Flask application initialization
app = Flask(__name__)
secret_key = os.getenv("SECRET_KEY")
app.secret_key = secret_key
app.config['SCHEDULER_API_ENABLED'] = True
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


# # check if current user exists in database
# def check_user_exist(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if session:
#             curr_user = User.objects(email=session['user']['email']).first()
#             if curr_user:
#                 return f(*args, **kwargs)
#             else:
#                 return redirect('/user/signout')
#     return wrap

@app.before_request
def check_user_existence():
    if request.endpoint == 'formula':
        if 'user' in session and 'email' in session['user']:
            user_email = session['user']['email']
            user = User.objects(email=user_email).first()

            if not user:
                # User is not found in the database, redirect to home
                return redirect(url_for('home'))


# @app.before_request
# def update_last_activity():
#     session.permanent = True
#     app.permanent_session_lifetime = timedelta(seconds=30)  # Setting the session timeout to 30 seconds
    # session['last_activity'] = datetime.utcnow()


# @app.before_request
# def check_last_activity():
#     if 'last_activity' in session:
#         last_activity_time = session['last_activity']
#         current_time = datetime.utcnow()
#         inactivity_duration = current_time - last_activity_time
#         max_inactivity_duration = timedelta(seconds=30)
#
#         if inactivity_duration > max_inactivity_duration:
#             # Redirect to the login page or another authentication route
#             return redirect(url_for('home'))

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
    user = User.objects(email=session['user']['email']).first()
    if user:
        data = {"session": session["logged_in"]}
    else:
        data = {"session": False}
    return jsonify(data)


# @app.get('/user')
# def presence():
#     if 'user' in session and session['user']['email']:
#         data = {"session": True}
#     else:
#         data = {"session": False}
#     return data


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

# Initialize the scheduler
scheduler = APScheduler()
scheduler.init_app(app)


# Define a function to reset daily limits for all users
def reset_daily_limits():
    users = User.objects()
    for user in users:
        user.reset_daily_limits()


# Use IntervalTrigger with a daily interval (24 hours)
scheduler.add_job(
    func=reset_daily_limits,
    trigger=IntervalTrigger(hours=24),
    id='reset_daily_limits',
    replace_existing=True,
)

# Run the scheduler
scheduler.start()
