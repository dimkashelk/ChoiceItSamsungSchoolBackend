from flask import Flask, request, jsonify
from data.session import *

app = Flask(__name__)
session = Session()


@app.route('/api/')
def hello_world():
    return 'Hello World!'


@app.route('/api/check_login')
def check_login():
    content = request.json
    print(f"GETTING {content['login']} TO CHECKING IS FREE")
    return jsonify({'is_free_login': session.check_login_free(content['login'])})


@app.route('/api/check_email')
def check_email():
    content = request.json
    print(f"GETTING {content['email']} TO CHECKING IS FREE")
    return jsonify({'is_free_email': session.check_email_free(content['email'])})


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


@app.route('/api/find_email')
def find_email():
    content = request.json
    return jsonify({'find': session.find_email(content['email'])})


if __name__ == '__main__':
    app.run()
