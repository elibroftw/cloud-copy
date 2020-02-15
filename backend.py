from flask import Flask, render_template, request, redirect, send_from_directory, send_file, url_for
from flask_compress import Compress
from werkzeug.middleware.proxy_fix import ProxyFix
from environs import Env
from pymongo import MongoClient
from passlib.hash import sha256_crypt
import os

Env().read_env()  # read from .env
DEVELOPMENT_SETTING = os.environ.get('DEBUG', '')
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 if DEVELOPMENT_SETTING else 604800
app.wsgi_app = ProxyFix(app.wsgi_app, num_proxies=1)
Compress(app)

client = MongoClient()
db = client.cloud_copy
users = db.users
# user structure
sample_user = {'email': 'cool_guy123@cool_domain.com',
               'devices': {'MAC': {'token': 'some-token',
                                   'last-login': 'date in server time'}},
               'tokens': {'token-value': 'MAC'}}


@app.route('/authenticate/', methods=['POST'])
def authenticate():
    # TODO: if not an email, forget password won't work
    # TODO: what if there is a space
    if request.method == 'POST':
        token, mac = request.args.get('token'), request.args.get('mac')
        email, password = request.args.get(
            'email'), request.args.get('password')
        if token:
            user = users.find({'mac': mac})
            user = users.find({'token': token})
        else:
            user = users.find({'email': email})
        if not user:  # user DNE
            password = sha256_crypt.encrypt(password)
            # hash password
            # create token
            # create new user
        else:
            sha256_crypt.verify(password, user['password'])
            pass
            # return new token

            # check if exists
            # check if correct

            # blind spots
            # last login should not be past 6 months
            # db should be cleaned every month or day at lowest peak
            # how to get peak?


@app.route('/connect/', methods=['POST'])
def connect():
    if request.method == 'POST':
        token, mac = request.args.get('token'), request.args.get('mac')
        email, password = request.args.get('email'), request.args.get('password')
        if token:
            user = users.find({'mac': mac})
            user = users.find({'token': token})
        else:
            user = users.find({'email': email})
        if not user:  # user DNE
            password = sha256_crypt.encrypt(password)
            # hash password
            # create token
            # create new user
        else:
            sha256_crypt.verify(password, user['password'])
            pass
            # return new token of 128-bit

            # check if exists
            # check if correct

            # blind spots
            # last login should not be past 6 months
            # db should be cleaned every month or day at lowest peak
            # how to get peak?


if __name__ == '__main__':
    assert os.path.exists('.env')
    app.run(debug=True, host='', port=5000)
