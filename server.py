from flask import Flask, request, jsonify, render_template
from flask_compress import Compress
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv
from pymongo import MongoClient
import base64
import bcrypt
import os
import secrets
from datetime import datetime
import json


load_dotenv()  # read from .env
DEVELOPMENT_SETTING = os.getenv('DEBUG')
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 if DEVELOPMENT_SETTING else 604800
app.wsgi_app = ProxyFix(app.wsgi_app, 1)
Compress(app)

client = MongoClient()
db = client.cloud_copy
users = db.users
tokens = db.tokens

# user structure
sample_user = {'email': 'cool_guy123@cool_domain.com',
               'devices': {'MAC': {'token': 'some-token',
                                   'last-login': 'date in server time'}},
               'tokens': {'token-value': 'MAC'}}


def hash_password(plain_text_password: str):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())


def check_password(plain_text_password: str, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)


@app.errorhandler(404)
def page_not_found(_):
    return render_template('home.html'), 404


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/authenticate/', methods=['POST'])
def authenticate():
    # TODO: if not an email, forget password won't work
    # TODO: what if there is a space
    if request.method == 'POST':
        if request.data: json_data = json.loads(request.data)
        else: json_data = request.values
        token, mac = json_data.get('token'), json_data.get('mac')
        email, password = json_data.get('email'), json_data.get('password')
        if token:
            token_obj = tokens.find_one({'token': token})
            if not token_obj: return 'invalid token'
            # if token is really old (6 months+) create a new one
            return token_obj['token']
        user = users.find_one({'email': email})
        if not user:  # user DNE; create new user
            hashed_password = hash_password(password)
            new_token = secrets.token_urlsafe()
            while tokens.find_one({'token': new_token}):
                new_token = secrets.token_urlsafe()
            tokens.insert_one({'token': new_token, 'email': email, 'created': datetime.today()})
            new_user = {'email': email, 'password': hashed_password, 'tokens': [new_token]}
            users.insert_one(new_user)
            return new_token
        else:  # user does exist
            if check_password(password, user['password']):
                new_token = secrets.token_urlsafe()
                while tokens.find_one({'token': new_token}):
                    new_token = secrets.token_urlsafe()
                tokens.insert_one({'token': new_token, 'email': email, 'created': datetime.today()})
                user_tokens = user['tokens'] + [new_token]
                users.update_one({'email': email}, {'$set': {'tokens': user_tokens}})
                return new_token
    return 'false'


@app.route('/share-copy/', methods=['POST'])
def share_copy():
    if request.method == 'POST':
        if request.data: json_data = json.loads(request.data)
        else: json_data = request.values
        token, contents = json_data.get('token'), json_data.get('contents')
        user = tokens.find_one({'token': token})
        if user:
            email = user['email']
            users.update_one({'email': email}, {'$set': {'current_copy': contents, 'updated': str(datetime.now())}})
            return 'true'
    return 'false'


@app.route('/newest-copy/', methods=['GET'])
def new_copies():
    if request.method == 'GET':
        token = request.args.get('token')
        user = tokens.find_one({'token': token})
        if user:
            email = user['email']
            user = users.find_one({'email': email})
            current_copy = user.get('current_copy')
            timestamp = user.get('updated')
            if current_copy:
                return jsonify({'current_copy': current_copy, 'timestamp': timestamp})
    return 'false'


# TODO: forgot password
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
