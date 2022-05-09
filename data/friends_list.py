import sqlalchemy
from sqlalchemy import ForeignKey

from .db_session import SqlAlchemyBase


class Friends(SqlAlchemyBase):
    __tablename__ = 'friends'

    id = sqlalchemy.Column(sqlalchemy.INTEGER, primary_key=True)
    id_first = sqlalchemy.Column(sqlalchemy.INTEGER, ForeignKey("user.id"))
    id_second = sqlalchemy.Column(sqlalchemy.INTEGER, ForeignKey("user.id"))
