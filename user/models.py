from flask import Flask, jsonify, request, session, redirect
from mongoengine.errors import NotUniqueError
from passlib.hash import pbkdf2_sha256
from user.history import User
from user import db
import uuid


class Users:
    def start_session(self, user):
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def signup(self):
        # create user object
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
        }

        # check if user exists already
        try:
            new_user = User()
            new_user._id = user['_id']
            new_user.name = user['name']
            new_user.email = user['email']
            new_user.password = pbkdf2_sha256.encrypt(request.form.get('password'))

            new_user.save()
            return self.start_session(user)
        except NotUniqueError as e:
            return jsonify({"error": "Email address already in Use"}), 400

    def signout(self):
        session.clear()
        # kill the database engine
        return redirect('/')

    def login(self):
        obj = User.objects(email=request.form.get("email")).first()

        if obj and pbkdf2_sha256.verify(request.form.get('password'), obj.password):
            # store user object in dictionary
            user = {
                "_id": str(obj.id),
                "name": obj.name,
                "email": obj.email,
            }
            return self.start_session(user)

        return jsonify({"error": "Invalid Login Credentials"}), 401
