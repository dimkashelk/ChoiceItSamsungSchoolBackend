from flask import Flask, request, jsonify
from data.session import *
import logging

app = Flask(__name__)
session = Session()

logging.basicConfig(level=logging.INFO, filename='/var/log/choiceit/app.log')


def presence_of_arguments(content, args):
    for i in args:
        if not content.get(i, False):
            return False
    return True


@app.route('/api/', methods=['POST', 'GET'])
def hello_world():
    return 'Hello World!'


@app.route('/api/check_login', methods=['POST', 'GET'])
def check_login():
    content = request.json
    if presence_of_arguments(content, ['login']):
        return jsonify({'is_free_login': session.check_login_free(content['login'])})
    else:
        return jsonify({'status': False})


@app.route('/api/check_email', methods=['POST', 'GET'])
def check_email():
    content = request.json
    if presence_of_arguments(content, ['email']):
        return jsonify({'is_free_email': session.check_email_free(content['email'])})
    else:
        return jsonify({'status': False})


@app.route('/api/auth', methods=['POST', 'GET'])
def check_data():
    content = request.json
    if presence_of_arguments(content, ['email']):
        print(f"GETTING email: {content['email']} password: {content['password']} TO CHECKING AUTH")
        res = session.authorization(content['email'], content['password'])
    elif presence_of_arguments(content, ['login']):
        print(f"GETTING login: {content['login']} password: {content['password']} TO CHECKING AUTH")
        res = session.authorization(content['login'], content['password'])
    else:
        return jsonify({'status': False})
    if res is None:
        return jsonify({
            'ok': False
        })
    return jsonify({
        'ok': True,
        'token': res[0],
        'login': res[1]
    })


@app.route('/api/find_email', methods=['POST', 'GET'])
def find_email():
    content = request.json
    if presence_of_arguments(content, ['email']):
        return jsonify({'find': session.find_email(content['email'])})
    else:
        return jsonify({'status': False})


@app.route('/api/check_verify_code', methods=['POST', 'GET'])
def check_verify_code():
    content = request.json
    if not presence_of_arguments(content, ['email', 'code', 'password']):
        return jsonify({
            'ok': False
        })
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


@app.route('/api/reg', methods=['POST', 'GET'])
def reg():
    content = request.json
    if not presence_of_arguments(content, ['email', 'first_name', 'password', 'login', 'second_name']):
        return jsonify({
            'status': False
        })
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
