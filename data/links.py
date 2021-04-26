import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
import random


class Link(SqlAlchemyBase):
    __tablename__ = 'links'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    key = sqlalchemy.Column(sqlalchemy.Integer)
    token = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    long_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    reply_at = sqlalchemy.Column(sqlalchemy.DateTime)
