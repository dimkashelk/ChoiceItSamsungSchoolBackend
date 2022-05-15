import sqlalchemy
from sqlalchemy import ForeignKey

from .db_session import SqlAlchemyBase


class Result(SqlAlchemyBase):
    __tablename__ = 'results'

    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    id_user = sqlalchemy.Column(sqlalchemy.INTEGER, ForeignKey("user.id"))
    id_survey = sqlalchemy.Column(sqlalchemy.INTEGER, ForeignKey("survey.id"))
