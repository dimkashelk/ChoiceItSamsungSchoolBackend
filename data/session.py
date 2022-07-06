import datetime
import io
import os

import bcrypt
import random
import string
import base64
from PIL import Image

from data import db_session
from data.user import User
from data.friends_list import Friends
from data.survey import Survey
from data.spot import Spot
from data.results import Result


def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password, hashed_password)


def random_word(length):
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    return ''.join(random.choice(letters) for _ in range(length))


class Session:

    def __init__(self):
        db_session.global_init('/home/dimkashelk/ChoiceItSamsungSchoolBackend/db/db.db')
        self.session = db_session.create_session()

    def check_login_free(self, login) -> bool:
        user = self.session.query(User).filter(User.login == login).first()
        return user is None

    def check_email_free(self, email) -> bool:
        user = self.session.query(User).filter(User.email == email).first()
        return user is None

    def get_token(self, user_id):
        user = self.session.query(User).filter(User.id == user_id).first()
        if user is None:
            return
        token = get_hashed_password(random_word(20).encode('utf-8') + user.login)
        user.token = token
        self.session.commit()
        return token

    def check_verify_code(self, email, code, password: str):
        user = self.session.query(User).filter(User.email == email).first()
        if user is not None:
            if user.verify_code == code:
                user.password = get_hashed_password(password.encode('utf-8'))
                token = get_hashed_password(random_word(20).encode('utf-8') + user.login.encode('utf-8'))
                user.token = token
                self.session.commit()
                return token, user.login

    def send_code(self, email, code):
        # TODO: send code to email
        return

    def find_email(self, email):
        user = self.session.query(User).filter(User.email == email).first()
        if user is not None:
            code = ''.join([str(random.randint(1, 10)) for _ in range(10)])
            user.verify_code = code
            self.session.commit()
            self.send_code(email, code)
            return True
        return False

    def registration(self, login, password, email, first_name, second_name):
        user_email = self.session.query(User).filter(User.email == email).first()
        user_login = self.session.query(User).filter(User.login == login).first()
        if user_email is not None or user_login is not None:
            return None, user_email is None, user_login is None
        user = User()
        user.email = email
        user.login = login
        user.first_name = first_name
        user.second_name = second_name
        user.password = get_hashed_password(password.encode('utf-8'))
        user.token = get_hashed_password(random_word(20).encode('utf-8') + user.login.encode('utf-8'))
        self.session.add(user)
        self.session.commit()
        return user.token, True, True

    def authorization(self, login, password):
        if '@' in login:
            user = self.session.query(User).filter(User.email == login).first()
        else:
            user = self.session.query(User).filter(User.login == login).first()
        if user is None:
            return
        if check_password(password.encode('utf-8'), user.password):
            user.token = get_hashed_password(random_word(20).encode('utf-8') + user.login.encode('utf-8'))
            self.session.commit()
            return str(user.token), user.login

    def check_token(self, login, token):
        user = self.session.query(User).filter(User.login == login).first()
        return user.token == token

    def load_friends(self, login):
        res = {}
        user = self.session.query(User).filter(User.login == login).first()
        friends = self.session.query(Friends).filter(Friends.id_first == user.id)
        res['count'] = friends.count()
        res['friends'] = []
        for row in friends:
            c_user = self.session.query(User).filter(User.id == row.id_first).first()
            count_surveys = self.session.query(Survey).filter(Survey.create_by == c_user.id)
            count_friends = self.session.query(Friends).filter(Friends.id_first == c_user.id)
            res['friends'].append({
                'id': c_user.id,
                'first_name': c_user.first_name,
                'second_name': c_user.second_name,
                'age': 0,
                'count_surveys': count_surveys.count(),
                'count_friends': count_friends.count()
            })
        return res

    def load_user_info(self, login):
        res = {'status': True}
        user = self.session.query(User).filter(User.login == login).first()
        if user == None:
            res['status'] = False
            return res
        friends = self.session.query(Friends).filter(Friends.id_first == user.id)
        surveys = self.session.query(Survey).filter(Survey.create_by == user.id)
        res['id'] = user.id
        res['login'] = user.login
        res['first_name'] = user.first_name
        res['second_name'] = user.second_name
        res['count_friends'] = friends.count()
        res['count_surveys'] = surveys.count()
        return res

    def load_person(self, person_id):
        res = {'status': False}
        user = self.session.query(User).filter(User.id == person_id).first()
        if user == None:
            res['status'] = True
            return res
        friends = self.session.query(Friends).filter(Friends.id_first == user.id)
        surveys = self.session.query(Survey).filter(Survey.create_by == user.id)
        res['id'] = user.id
        res['login'] = user.login
        res['first_name'] = user.first_name
        res['second_name'] = user.second_name
        res['count_friends'] = friends.count()
        res['count_surveys'] = surveys.count()
        return res

    def load_search_person(self, person_name):
        res = {}
        users = self.session.query(User).filter((User.first_name + User.second_name).like(f'%{person_name}%'))
        res['count'] = users.count()
        res['persons'] = []
        for row in users:
            res['persons'].append(self.load_person(row.id))
        return res

    def upload_survey(self, content):
        user = self.session.query(User).filter(User.login == content['login']).first()
        survey = Survey()
        survey.create_by = user.id
        survey.title = content['title']
        survey.description = content['description']
        survey.is_archive = False
        survey.is_favorites = content['add_to_favorites']
        survey.only_for_friends = content['only_for_friends']
        survey.to_date = content['to_date']
        survey.create_date = int(datetime.datetime.now().timestamp())
        self.session.add(survey)
        self.session.commit()
        for i in content['images']:
            spot = Spot()
            spot.title = i['title']
            spot.id_survey = survey.id
            self.session.add(spot)
            self.session.commit()
            img_bytes = base64.b64decode(i['image'].encode('utf-8'))
            img = Image.open(io.BytesIO(img_bytes))
            img.save('C:\\Users\\shelk\\PycharmProjects\\ChoiceItSamsungSchoolBackend\\db\\images\\spots\\' + str(
                spot.id) + '.png')
        return {'status': True}

    def check_auth_token(self, login, token):
        user = self.session.query(User).filter(User.login == login).first()
        return str(user.token) == token

    def update_user_data(self, content):
        res = {}
        user = self.session.query(User).filter(User.login == content['login']).first()
        if 'new_profile_image' in content:
            if os.path.isfile(f'../db/images/profile/{user.login}.png'):
                os.remove(f'../db/images/profile/{user.login}.png')
            img_bytes = base64.b64decode(content['new_profile_image'].encode('utf-8'))
            img = Image.open(io.BytesIO(img_bytes))
            img.save('C:\\Users\\shelk\\PycharmProjects\\ChoiceItSamsungSchoolBackend\\db\\images\\profile\\' + str(
                user.login) + '.png')
        user.login = content['new_login']
        user.first_name = content['first_name']
        user.second_name = content['second_name']
        if 'new_password' in content:
            user.password = get_hashed_password(content['new_password'].encode('utf-8'))
            user.token = get_hashed_password(random_word(20).encode('utf-8') + user.login.encode('utf-8'))
        self.session.query(User).update(user)
        self.session.commit()
        res['login'] = user.login
        res['token'] = user.token
        return res

    def search(self, content):
        res = {
            'count_surveys': 0,
            'count_persons': 0,
            'persons': [],
            'surveys': []
        }
        user = self.session.query(User).filter(User.login == content['login']).first()
        if content['search_persons']:
            persons = self.session.query(User).filter(
                (User.first_name + User.second_name).like(f"%{content['value']}%"),
                User.age >= content['age_from'],
                User.age <= content['age_to'])
            res['count_persons'] = len(persons)
            for row in persons:
                res['persons'].append({
                    'person_id': row.id,
                    'first_name': row.first_name,
                    'second_name': row.second_name
                })
        if content['search_surveys']:
            if 'search_friends_surveys' in content:
                if content['search_friends_surveys']:
                    friends_list = self.session.query(Friends).filter(Friends.id_first == user.id)
                    friends_id = [i.id_second for i in friends_list]
                    friends = self.session.query(User).filter(User.id.in_(friends_id))
                    surveys = self.session.query(Survey).filter(
                        Survey.title.like(f"%{content['value']}%"),
                        Survey.count_spots >= content['count_question_from'],
                        Survey.count_spots <= content['count_question_to'],
                        Survey.create_by.in_([i.id for i in friends])
                    )
                else:
                    surveys = self.session.query(Survey).filter(
                        Survey.title.like(f"%{content['value']}%"),
                        Survey.count_spots >= content['count_question_from'],
                        Survey.count_spots <= content['count_question_to'],
                    )
            else:
                surveys = self.session.query(Survey).filter(
                    Survey.title.like(f"%{content['value']}%"),
                    Survey.count_spots >= content['count_question_from'],
                    Survey.count_spots <= content['count_question_to'],
                )
            res['count_surveys'] = len(surveys)
            for row in surveys:
                res['surveys'].append({
                    'survey_id': row.id,
                    'title': row.title,
                    'description': row.description,
                    'person_url': row.create_by
                })
        return res

    def save_res_survey(self, content):
        user = self.session.query(User).filter(User.login == content['login']).first()
        survey = self.session.query(Survey).filter(Survey.id == content['survey']['survey_id']).first()
        survey.count_res += 1
        self.session.query(Survey).update(survey)
        self.session.commit()
        count_place = len(set(i['place'] for i in content['survey']['spots']))
        for spot in content['survey']['spots']:
            spot['place'] = count_place + 1 - spot['place']
        for spot in content['survey']['spots']:
            dop_spot = self.session.query(Spot).filter(Spot.id == spot['id']).first()
            dop_spot.count_voice += spot['place']
            self.session.query(dop_spot).update(dop_spot)
            self.session.commit()
        res = Result()
        res.id_user = user.id
        res.id_survey = survey.id
        self.session.add(res)
        self.session.commit()
        return {'status': True}

    def add_to_friends(self, user_login, person_id):
        user = self.session.query(User).filter(User.login == user_login).first()
        person = self.session.query(User).filter(User.id == person_id).first()
        friends = Friends()
        friends.id_first = user.id
        friends.id_second = person.id
        self.session.add(friends)
        self.session.commit()

    def remove_friend(self, user_login, person_id):
        user = self.session.query(User).filter(User.login == user_login).first()
        person = self.session.query(User).filter(User.id == person_id).first()
        self.session.query(Friends).filter(Friends.id_first == user.id, Friends.id_second == person.id).delete()
        self.session.commit()
        return {'status': True}

    def load_news_feed(self,
                       login,
                       friends,
                       min_count,
                       max_count,
                       sort_most_popular,
                       sort_date,
                       decreasing):
        user = self.session.query(User).filter(User.login == login).first()
        res = {
            'news': [],
            'count': 0
        }
        max_count_surveys = 100
        if friends.size() > 0:
            d = list(map(int, friends))
            surveys = self.session.query(Survey).filter(Survey.create_by.in_(d))
        else:
            surveys = self.session.query(Survey).all()
        filtered_surveys = []
        survey_which_user_completed = self.session.query(Result.id_survey).filter(Result.id_user == user.id)
        for row in surveys:
            if min_count <= row.count_spots - (row.count_spots + 1) % 2 <= max_count and \
                    row.id not in survey_which_user_completed:
                filtered_surveys.append(row)
        if sort_most_popular:
            survey_id = [row.id for row in filtered_surveys]
            results = self.session.query(Result).filter(Result.id_survey.in_(survey_id))
            most_popular = {}
            for row in results:
                most_popular[row.id_survey] = most_popular.get(row.id_survey, 0) + 1
            filtered_surveys.sort(key=lambda x: most_popular[x.id], reverse=decreasing)
        elif sort_date:
            filtered_surveys.sort(key=lambda x: x.create_date, reverse=decreasing)
        surveys_to_send = filtered_surveys[:max_count_surveys]
        for survey in surveys_to_send:
            res['news'].append({
                'id': survey.id,
                'title': survey.title,
                'description': survey.description,
                'title_image_url': '',
                'person_url': survey.create_by
            })
        res['count'] = len(res['news'])
        return res

    def user_surveys(self, login):
        user = self.session.query(User).filter(User.login == login).first()
        res = {
            'surveys': [],
            'count': 0
        }
        surveys = self.session.query(Survey).filter(Survey.create_by == user.id).all()
        res['count'] = len(surveys)
        for survey in surveys:
            res['surveys'].append({
                'id': survey.id,
                'title': survey.title,
                'description': survey.description,
                'title_image_url': '',
                'person_url': survey.create_by,
                'is_archive': survey.is_archive,
                'is_favorite': survey.is_favorites
            })
        return res
