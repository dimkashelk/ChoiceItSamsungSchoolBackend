import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'user'

    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    first_name = sqlalchemy.Column(sqlalchemy.String)
    second_name = sqlalchemy.Column(sqlalchemy.String)
    verify_code = sqlalchemy.Column(sqlalchemy.INTEGER)
    password = sqlalchemy.Column(sqlalchemy.String)
    token = sqlalchemy.Column(sqlalchemy.String)
