from data import db_session
from .user import User
import bcrypt


def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password, hashed_password)


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

    def check_verify_code(self, email, code, password: str):
        user = self.session.query(User).filter(User.email == email).first()
        if user is not None:
            if user.verify_code == code:
                user.password = get_hashed_password(password.encode('utf-8'))
                self.session.commit()
