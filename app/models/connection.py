"""
    UFind-API.connection
    
    :copyright: (c) Apr 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.
"""
from peewee import *

from . import BaseModel
from app.models.user import User


class Connection(BaseModel):
    """
    Represents a connection between two users.
    """
    user_a = ForeignKeyField(User, backref="userA")
    user_b = ForeignKeyField(User, backref="userB")

    def __repr__(self):
        return "<Connection: {} -> {}>".format(self.user_a, self.user_b)

    def to_dict(self):
        return {
            "user_a": self.user_a.to_dict(),
            "user_b": self.user_b.to_dict(),
        }

    @staticmethod
    def connect(user_a, user_b):
        """
        Make a connection between the two users.
        :param user_a:
        :param user_b:
        :return:
        """
        if not Connection.already_connected(user_a, user_b):
            return Connection.create(
                user_a=user_a,
                user_b=user_b,
            )
        else:
            raise Connection.Duplicate

    @staticmethod
    def already_connected(user_a, user_b):
        """
        Check if user A is connected to user B.
        :param user_a:
        :param user_b:
        :return: bool
        """
        it = Connection.select().where(
            (Connection.user_a == user_a.id & Connection.user_b == user_b.id) |
            (Connection.user_a == user_b.id & Connection.user_b == user_a.id)
        )
        return it.first() is not None

    @staticmethod
    def by_user(user_id):
        """
        Get all the connections made by a user.
        :param user_id:
        :return:
        """
        it = Connection.select()
        return list(
            map(lambda conn: conn.to_dict(),
                filter(lambda conn: conn.user_a.id == user_id
                                    or conn.user_b.id == user_id, it)))

    class Duplicate(Exception):
        pass
