from flask import Flask, request, jsonify, send_from_directory
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


@app.route('/api/friends', methods=['POST'])
def load_friends():
    content = request.json
    if not presence_of_arguments(content, ['login', 'token']):
        return jsonify({
            'status': False
        })
    if not session.check_token(login=content['login'], token=content['token']):
        return jsonify({
            'status': False
        })
    res = session.load_friends(content['login'])
    return jsonify(res)


@app.route('/api/user', methods=['POST'])
def load_user_info():
    content = request.json
    if not presence_of_arguments(content, ['login', 'token']):
        return jsonify({
            'status': False
        })
    if not session.check_token(login=content['login'], token=content['token']):
        return jsonify({
            'status': False
        })
    res = session.load_user_info(content['login'])
    return jsonify(res)


@app.route('/api/load_person', methods=['POST'])
def load_person():
    content = request.json
    if not presence_of_arguments(content, ['login', 'token', 'person']):
        return jsonify({
            'status': False
        })
    if not session.check_token(login=content['login'], token=content['token']):
        return jsonify({
            'status': False
        })
    res = session.load_person(content['person'])
    return jsonify(res)


@app.route('/api/load_search_person', methods=['POST'])
def load_search_person():
    content = request.json
    if not presence_of_arguments(content, ['login', 'token', 'person']):
        return jsonify({
            'status': False
        })
    if not session.check_token(login=content['login'], token=content['token']):
        return jsonify({
            'status': False
        })
    res = session.load_search_person(content['person'])
    return jsonify(res)


@app.route('/api/images/<int:person_id>', methods=['POST'])
def load_person_image(person_id):
    content = request.json
    if not presence_of_arguments(content, ['login', 'token']):
        return jsonify({
            'status': False
        })
    if not session.check_token(login=content['login'], token=content['token']):
        return jsonify({
            'status': False
        })
    return send_from_directory(
        './db/images/profile/',
        f'{person_id}' + '_profile.png',
        as_attachment=True,
        attachment_filename='profile.png'
    )


if __name__ == '__main__':
    app.run()

# TODO: /api/user_news_feed POST login, token, friends (LIST<String>), min_count, max_count, is_increasing_most_popular,
#  is_increasing_active, is_increasing_date - load user news feed
# TODO: /api/search POST login, token, value, search_persons, search_surveys, search_friends_surveys, age_from, age_to,
#  count_question_from, count_question_to - search surveys and persons by name
# TODO: /api/user_surveys/{survey_id} POST login, token, is_title - load survey title image
# TODO: /api/load_person/{person_id} POST login, token, profile - load user image
# TODO: /api/load_survey/{survey_id} POST login, token, survey - load survey title image
# TODO: /api/save_res_survey POST login, token, survey {survey_id, spots {spot_id, place}} - save results of survey
# TODO: /api/update_user_data POST new_login, first_name, second_name, login, token, old_password (option),
#  new password (option), new_profile_image (option) - update user info
# TODO: /api/upload_survey POST login, token, images (list), to_date, add_to_favorites, only_for_friends,
#  anonymous_statistic,  send_to_friends, title, description - upload survey to server
