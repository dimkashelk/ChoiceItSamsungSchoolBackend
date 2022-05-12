import sqlalchemy
from sqlalchemy import ForeignKey

from .db_session import SqlAlchemyBase


class Spot(SqlAlchemyBase):
    __tablename__ = 'spots'

    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    id_survey = sqlalchemy.Column(sqlalchemy.INTEGER, ForeignKey('survey.id'))
    count_voice = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
