import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'user'

    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True)
    login_lower = sqlalchemy.Column(sqlalchemy.String, unique=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    first_name = sqlalchemy.Column(sqlalchemy.String)
    first_name_lower = sqlalchemy.Column(sqlalchemy.String)
    second_name = sqlalchemy.Column(sqlalchemy.String)
    second_name_lower = sqlalchemy.Column(sqlalchemy.String)
    verify_code = sqlalchemy.Column(sqlalchemy.INTEGER)
    password = sqlalchemy.Column(sqlalchemy.BLOB)
    token = sqlalchemy.Column(sqlalchemy.BLOB)
    age = sqlalchemy.Column(sqlalchemy.INTEGER, default=1)
