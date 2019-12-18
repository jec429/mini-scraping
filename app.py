import numpy as np
from flask import Flask, redirect, url_for, render_template, request, Response, abort
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_utils import *
import json
import pickle
import pandas as pd
import multiprocessing as mp


app = Flask(__name__)
app.url_map.converters['list'] = ListConverter

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/main_search')
@login_required
def main_search():
    return render_template('main_search.html')


# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_entry = User.get(username)
        if user_entry is not None:
            user = User(user_entry[0], user_entry[1])
            if user.password == password:
                login_user(user)
                return redirect(url_for('main_search'))
            else:
                return abort(401)
        else:
            return abort(401)
    else:
        return Response('''
        <form action="" method="post">
            Username:<br>
            <p><input type=text name=username>
            <br>
            Password:<br>
            <p><input type=password name=password>
            <br><br>
            <p><input type=submit value=Login>
        </form>
        ''')


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('logout.html')


# handle login failed
@app.errorhandler(401)
def page_not_found():
    return render_template('login_failed.html')


# callback to reload the user object
@login_manager.user_loader
def load_user(username):
    user_entry = User.get(username)
    return User(user_entry[0], user_entry[1])


if __name__ == '__main__':
    app.config["SECRET_KEY"] = "ITSANOTHERSECRET"
    app.run(debug=True, port=5000)
