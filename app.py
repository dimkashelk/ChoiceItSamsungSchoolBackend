from flask import Flask, request, jsonify
from data.session import *

app = Flask(__name__)


@app.route('/api/')
def hello_world():
    return 'Hello World!'


@app.route('/api/check_login')
def check_login():
    content = request.json
    print(f"GETTING {content['login']} TO CHECKING IS FREE")
    return jsonify({'is_free': True})


@app.route('/api/check_email')
def check_email():
    content = request.json
    print(f"GETTING {content['email']} TO CHECKING IS FREE")
    return jsonify({'is_free': True})


@app.route('/api/auth')
def check_data():
    content = request.json
    if content.get('email', False):
        print(f"GETTING email: {content['email']} password: {content['password']} TO CHECKING AUTH")
    else:
        print(f"GETTING login: {content['login']} password: {content['password']} TO CHECKING AUTH")
    return jsonify({'status': 'ok',
                    'login': 'dimkashelk',
                    'token': hash('Hello, world!')})


if __name__ == '__main__':
    token = get_hashed_password(randbytes(50))
    print(token)
    # app.run()
