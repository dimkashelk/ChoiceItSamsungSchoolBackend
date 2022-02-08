from data import user, db_session


class Session:

    def __init__(self):
        db_session.global_init('./db/db.db')
        self.session = db_session.create_session()
