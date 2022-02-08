from data import db_session
from user import User


class Session:

    def __init__(self):
        db_session.global_init('./db/db.db')
        self.session = db_session.create_session()

    def check_login(self, login) -> bool:
        user = self.session.query(User).filter(User.login == login).first()
        return user is not None
