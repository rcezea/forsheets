from app import app, jsonify
from user.models import Users


@app.post('/user/signup')
def signup():
    try:
        return Users().signup()
    except Exception as e:
        return jsonify({"error": e}), 401


@app.route('/user/signout')
def signout():
    return Users().signout()


@app.post('/user/login')
def login():
    try:
        return Users().login()
    except Exception as e:
        return jsonify({"error": e}), 401
