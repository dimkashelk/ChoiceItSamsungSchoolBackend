from flask import Flask, request, jsonify, send_from_directory
from data.session import *
import logging

app = Flask(__name__)
session = Session()


# logging.basicConfig(level=logging.INFO, filename='/var/log/choiceit/app.log')


def presence_of_arguments(content, args):
    try:
        for i in args:
            if i not in content:
                return False
    except BaseException:
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
    if presence_of_arguments(content, ['login', 'token']):
        return jsonify({
            'ok': session.check_auth_token(content['login'], content['token'])
        })
    elif presence_of_arguments(content, ['email', 'password']):
        res = session.authorization(content['email'], content['password'])
    elif presence_of_arguments(content, ['login', 'password']):
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


@app.route('/api/check_token', methods=['POST'])
def check_token():
    content = request.json
    if not presence_of_arguments(content, ['login', 'token']):
        return jsonify({
            'ok': False
        })
    if not session.check_auth_token(login=content['login'], token=content['token']):
        return jsonify({
            'ok': False
        })
    return jsonify({'ok': True})


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
        'token': str(res[0])
    })


@app.route('/api/friends', methods=['POST'])
def load_friends():
    content = request.json
    if not presence_of_arguments(content, ['login', 'token']):
        return jsonify({
            'status': False
        })
    if not session.check_auth_token(login=content['login'], token=content['token']):
        return jsonify({
            'status': False
        })
    res = session.load_friends(content['login'])
    res['status'] = True
    return jsonify(res)


@app.route('/api/user', methods=['POST'])
def load_user_info():
    content = request.json
    if not presence_of_arguments(content, ['login', 'token']):
        return jsonify({
            'status': False
        })
    if not session.check_auth_token(login=content['login'], token=content['token']):
        return jsonify({
            'status': False
        })
    res = session.load_user_info(content['login'])
    res['status'] = True
    return jsonify(res)


@app.route('/api/load_person', methods=['POST'])
def load_person():
    content = request.json
    if not presence_of_arguments(content, ['login', 'token', 'person']):
        return jsonify({
            'status': False
        })
    if not session.check_auth_token(login=content['login'], token=content['token']):
        return jsonify({
            'status': False
        })
    res = session.load_person(content['person'])
    res['status'] = True
    return jsonify(res)


@app.route('/api/load_search_person', methods=['POST'])
def load_search_person():
    content = request.json
    if not presence_of_arguments(content, ['login', 'token', 'person']):
        return jsonify({
            'status': False
        })
    if not session.check_auth_token(login=content['login'], token=content['token']):
        return jsonify({
            'status': False
        })
    res = session.load_search_person(content['person'])
    res['status'] = True
    return jsonify(res)


@app.route('/api/images/<int:person_id>', methods=['POST'])
def load_person_image(person_id):
    content = request.json
    if not presence_of_arguments(content, ['login', 'token']):
        return jsonify({
            'status': False
        })
    if not session.check_auth_token(login=content['login'], token=content['token']):
        return jsonify({
            'status': False
        })
    return send_from_directory(
        './db/images/profile/',
        f'{person_id}' + '_profile.png',
        as_attachment=True,
        attachment_filename='profile.png'
    )


@app.route('/api/user_surveys/<int:survey_id>', methods=['POST'])
def load_survey_image(survey_id):
    content = request.json
    if not presence_of_arguments(content, ['login', 'token']):
        return jsonify({
            'status': False
        })
    if not session.check_auth_token(login=content['login'], token=content['token']):
        return jsonify({
            'status': False
        })
    return send_from_directory(
        './db/images/survey/',
        f'{survey_id}' + '_title.png',
        as_attachment=True,
        attachment_filename='title.png'
    )


@app.route('/api/load_person/<int:person_id>', methods=['POST'])
def load_image(person_id):
    content = request.json
    if not presence_of_arguments(content, ['login', 'token']):
        return jsonify({
            'status': False
        })
    if not session.check_auth_token(login=content['login'], token=content['token']):
        return jsonify({
            'status': False
        })
    return send_from_directory(
        './db/images/profile/',
        f'{person_id}' + '_profile.png',
        as_attachment=True,
        attachment_filename='profile.png'
    )


@app.route('/api/user_surveys', methods=['POST'])
def user_surveys():
    content = request.json
    if not presence_of_arguments(content, ['login', 'token']):
        return jsonify({
            'status': False
        })
    if not session.check_auth_token(login=content['login'], token=content['token']):
        return jsonify({
            'status': False
        })
    res = session.user_surveys(content['login'])
    res['status'] = True
    return jsonify(res)


@app.route('/api/load_survey', methods=['POST'])
def load_survey_image_():
    content = request.json
    if not presence_of_arguments(content, ['login', 'token', 'survey_id']):
        return jsonify({
            'status': False
        })
    if not session.check_auth_token(login=content['login'], token=content['token']):
        return jsonify({
            'status': False
        })
    res = session.load_survey(content['survey_id'])
    res['status'] = True
    return jsonify(res)


@app.route('/api/upload_survey', methods=['POST'])
def upload_survey():
    content = request.json
    if not presence_of_arguments(content, ['login',
                                           'token',
                                           'images',
                                           'to_date',
                                           'add_to_favorites',
                                           'only_for_friends',
                                           'anonymous_statistic',
                                           'send_to_friends',
                                           'title',
                                           'description']):
        return jsonify({
            'status': False
        })
    if not session.check_auth_token(login=content['login'], token=content['token']):
        return jsonify({
            'status': False
        })
    res = session.upload_survey(content)
    res['status'] = True
    return jsonify(res)


@app.route('/api/update_user_data', methods=['POST'])
def update_user_data():
    content = request.json
    if not presence_of_arguments(content, ['new_login', 'first_name', 'second_name', 'login', 'token']):
        return jsonify({
            'status': False
        })
    if not session.check_auth_token(login=content['login'], token=content['token']):
        return jsonify({
            'status': False
        })
    res = session.update_user_data(content)
    res['status'] = True
    return jsonify(res)


@app.route('/api/search', methods=['POST'])
def search():
    content = request.json
    if not presence_of_arguments(content, [
        'login',
        'token',
        'value',
        'search_persons',
        'search_surveys',
        'search_friends_surveys',
        'age_from',
        'age_to',
        'count_question_from',
        'count_question_to'
    ]):
        return jsonify({
            'status': False
        })
    if not session.check_auth_token(login=content['login'], token=content['token']):
        return jsonify({
            'status': False
        })
    res = session.search(content)
    res['status'] = True
    return jsonify(res)


@app.route('/api/save_res_survey', methods=['POST'])
def save_res_survey():
    content = request.json
    if not presence_of_arguments(content, [
        'login',
        'token',
        'survey'
    ]):
        return jsonify({
            'status': False
        })
    if not session.check_auth_token(login=content['login'], token=content['token']):
        return jsonify({
            'status': False
        })
    res = session.save_res_survey(content)
    return jsonify(res)


@app.route('/api/add_to_friends', methods=['POST'])
def add_to_friends():
    content = request.json
    if not presence_of_arguments(content, [
        'login',
        'token',
        'person_id'
    ]):
        return jsonify({
            'status': False
        })
    if not session.check_auth_token(login=content['login'], token=content['token']):
        return jsonify({
            'status': False
        })
    res = session.add_to_friends(content['login'], content['person_id'])
    return jsonify(res)


@app.route('/api/remove_friend', methods=['POST'])
def remove_friends():
    content = request.json
    if not presence_of_arguments(content, [
        'login',
        'token',
        'person_id'
    ]):
        return jsonify({
            'status': False
        })
    if not session.check_auth_token(login=content['login'], token=content['token']):
        return jsonify({
            'status': False
        })
    res = session.remove_friend(content['login'], content['person_id'])
    return jsonify(res)


@app.route('/api/user_news_feed', methods=['POST'])
def user_news_feed():
    content = request.json
    if not presence_of_arguments(content, [
        'login',
        'token',
        'friends',
        'min_count',
        'max_count',
        'sort_most_popular',
        'sort_date',
        'decreasing'
    ]):
        return jsonify({
            'status': False
        })
    if not session.check_auth_token(login=content['login'], token=content['token']):
        return jsonify({
            'status': False
        })
    res = session.load_news_feed(
        login=content['login'],
        friends=content['friends'],
        min_count=content['min_count'],
        max_count=content['max_count'],
        sort_most_popular=content['sort_most_popular'],
        sort_date=content['sort_date'],
        decreasing=content['decreasing']
    )
    res['status'] = True
    return jsonify(res)


@app.route('/api/images/survey_title', methods=['POST'])
def load_survey_title():
    content = request.json
    if not presence_of_arguments(content, [
        'login',
        'token',
        'survey_id'
    ]):
        return jsonify({
            'status': False
        })
    if not session.check_auth_token(login=content['login'], token=content['token']):
        return jsonify({
            'status': False
        })
    return jsonify(session.load_survey_title_image(content['survey_id']))


@app.route('/api/images/person', methods=['POST'])
def load_image_person():
    content = request.json
    if not presence_of_arguments(content, [
        'login',
        'token',
        'person_id'
    ]):
        return jsonify({
            'status': False
        })
    if not session.check_auth_token(login=content['login'], token=content['token']):
        return jsonify({
            'status': False
        })
    return jsonify(session.load_person_image(content['person_id']))


if __name__ == '__main__':
    app.run()
