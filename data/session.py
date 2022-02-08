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
        db_session.global_init('./db/db.db')
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
        token = get_hashed_password(random_word(20).encode('utf-8'))
        user.token = token
        self.session.commit()
        return token

    def check_verify_code(self, email, code, password: str):
        user = self.session.query(User).filter(User.email == email).first()
        if user is not None:
            if user.verify_code == code:
                user.password = get_hashed_password(password.encode('utf-8'))
                token = get_hashed_password(random_word(20).encode('utf-8'))
                user.token = token
                self.session.commit()
                return token

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
