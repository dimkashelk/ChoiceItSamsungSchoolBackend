import sqlalchemy
from sqlalchemy import ForeignKey

from .db_session import SqlAlchemyBase


class Survey(SqlAlchemyBase):
    __tablename__ = 'survey'

    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    create_by = sqlalchemy.Column(sqlalchemy.INTEGER, ForeignKey("user.id"))
    is_archive = sqlalchemy.Column(sqlalchemy.BOOLEAN)
    is_favorites = sqlalchemy.Column(sqlalchemy.BOOLEAN)
