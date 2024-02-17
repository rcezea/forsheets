from flask import Flask
from app import app
from user.models import Users


@app.post('/user/signup')
def signup():
    return Users().signup()


@app.route('/user/signout')
def signout():
    return Users().signout()


@app.post('/user/login')
def login():
    return Users().login()
