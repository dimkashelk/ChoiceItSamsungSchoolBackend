import sqlalchemy
from sqlalchemy import ForeignKey

from .db_session import SqlAlchemyBase


class Survey(SqlAlchemyBase):
    __tablename__ = 'survey'

    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    title_lower = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    description_lower = sqlalchemy.Column(sqlalchemy.String)
    create_by = sqlalchemy.Column(sqlalchemy.INTEGER, ForeignKey("user.id"))
    create_date = sqlalchemy.Column(sqlalchemy.INTEGER)
    is_archive = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)
    is_favorites = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)
    only_for_friends = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)
    to_date = sqlalchemy.Column(sqlalchemy.INTEGER, default=-1)
    count_spots = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
    count_res = sqlalchemy.Column(sqlalchemy.INTEGER, default=0)
