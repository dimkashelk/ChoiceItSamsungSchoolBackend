import sqlalchemy
from sqlalchemy import ForeignKey

from .db_session import SqlAlchemyBase


class Survey(SqlAlchemyBase):
    __tablename__ = 'survey'

    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    create_by = sqlalchemy.Column(sqlalchemy.INTEGER, ForeignKey("user.id"))
    is_archive = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)
    is_favorites = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)
    only_for_friends = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)
    to_date = sqlalchemy.Column(sqlalchemy.INTEGER, default=-1)
