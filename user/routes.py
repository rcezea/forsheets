from app import app, jsonify
from user.models import Users


@app.post('/user/signup')
def signup():
    return Users().signup()


@app.route('/user/signout')
def signout():
    return Users().signout()


@app.post('/user/login')
def login():
    try:
        return Users().login()
    except Exception as e:
        return jsonify({"error": e}), 401
