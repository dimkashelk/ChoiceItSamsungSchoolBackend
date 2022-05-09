import bcrypt
import random
import string

from data import db_session
from data.user import User


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
            return user.token, user.login

    def check_token(self, login, token):
        user = self.session.query(User).filter(User.login == login).first()
        return user.token == token

