from flask import Flask, render_template, session, redirect, request
from functools import wraps
from formulai import generate, lecture
from user.models import User
from user import db

app = Flask(__name__)
app.secret_key = b'\xcf\xda\xa5\xc5#\xfa\xb6\xc7\x91\xc7\xdc\x13c\xe8x\xc3'

# start the database engine
db.start_db()


# Decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/home')

    return wrap


# routes
from user import routes


@app.route('/')
@login_required
def application():
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


@app.get('/formula')
def formula():
    user_input = request.args.get('user_input')
    if user_input == "":
        return "Please enter text"
    message = generate(user_input)

    # Update users' history
    if 'user' in session:
        user = User.objects(email=session['user']['email']).first()
        user.add_to_history(user_input, message[1:])

    return message


@app.route('/explain', strict_slashes=False, methods=['GET'])
def explain():
    user_input = request.args.get('user_input')
    # if user_input == "Please enter text":
    #     return "This is your last warning"
    message = lecture(user_input)
    return message
