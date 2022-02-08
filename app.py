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
    return jsonify({'is_free_login': session.check_login_free(content['login'])})


@app.route('/api/check_email')
def check_email():
    content = request.json
    return jsonify({'is_free_email': session.check_email_free(content['email'])})


@app.route('/api/auth')
def check_data():
    content = request.json
    if content.get('email', False):
        print(f"GETTING email: {content['email']} password: {content['password']} TO CHECKING AUTH")
        res = session.authorization(content['email'], content['password'])
    else:
        print(f"GETTING login: {content['login']} password: {content['password']} TO CHECKING AUTH")
        res = session.authorization(content['login'], content['password'])
    if res is None:
        return jsonify({
            'ok': False
        })
    return jsonify({
        'ok': True,
        'token': res[0],
        'login': res[1]
    })


@app.route('/api/find_email')
def find_email():
    content = request.json
    return jsonify({'find': session.find_email(content['email'])})


@app.route('/api/check_verify_code')
def check_verify_code():
    content = request.json
    res = session.check_verify_code(
        content['email'],
        content['code'],
        content['password']
    )
    if res is not None:
        return jsonify({
            'ok': True,
            'token': res[0],
            'login': res[1]
        })
    return jsonify({
        'ok': False
    })


@app.route('/api/reg')
def reg():
    content = request.json
    res = session.registration(
        content['login'],
        content['password'],
        content['email'],
        content['first_name'],
        content['second_name']
    )
    if res[0] is None:
        return jsonify({
            'status': False,
            'email_free': res[1],
            'login_free': res[2]
        })
    return jsonify({
        'status': True,
        'token': res[0]
    })


if __name__ == '__main__':
    app.run()
