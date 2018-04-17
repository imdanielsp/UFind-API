"""
    UFind-API.subscription
    
    :copyright: (c) Apr 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.
"""
from peewee import *

from . import BaseModel
from app.models.user import User
from app.models.category import Category
from app.models.connection import Connection


class Subscription(BaseModel):
    """
    Represents a subscription.
    """
    category = ForeignKeyField(Category, backref="categories")
    user = ForeignKeyField(User, backref="users")

    def __repr__(self):
        return "<Subscription: {} -> {}>".format(self.user, self.category)

    @staticmethod
    def subscribe(email, category_id):
        category = Category.by_id(category_id)

        try:
            Subscription.find_subscription(email, category_id)
        except Subscription.NotFound:
            subs = Subscription.create(
                user=User.get_user_by_email(email),
                category=category
            )
        else:
            raise Subscription.Duplicate

        category.increment()

        return subs

    @staticmethod
    def unsubscribe(email, category_id):
        category = Category.by_id(category_id)

        subs = Subscription.find_subscription(email, category_id)
        subs.delete_instance()

        category.decrement()

    @staticmethod
    def find_subscription(email, category_id):
        user = User.get_user_by_email(email)

        subscription = Subscription.select().where(
            Subscription.user == user.id).where(
            Subscription.category == category_id).first()

        if not subscription:
            raise Subscription.NotFound

        return subscription

    @staticmethod
    def intersection_with(user_id):
        subscriptions = Subscription.by_user(user_id)

        users = set()

        for subs in subscriptions:
            for subs2 in Subscription.by_category(subs.category.id):
                if subs2.user.id is not user_id:
                    users.add(subs2.user)

        conns = Connection.select().where(
            Connection.user_a == user_id or Connection.user_b == user_id
        )

        discoverable = set()

        for user in users:
            is_connection = False

            for conn in conns:
                if conn.user_a.id == user.id or conn.user_b.id == user.id and \
                        conn.user_a.id == user_id or conn.user_b.id == user_id:
                    is_connection = True

            if not is_connection:
                discoverable.add(user)

        return discoverable

    def to_dict(self):
        user = self.user.to_safe_dict()
        user.pop("profile_image")
        return {
            "category": self.category.to_dict(),
            "user": user
        }

    def to_dict_without_user(self):
        return self.to_dict()["category"]

    class NotFound(Exception):
        pass

    class Duplicate(Exception):
        pass

    @staticmethod
    def by_user_to_dict(user_id):
        return list(map(lambda sub: sub.to_dict_without_user(),
                        Subscription.by_user(user_id)))

    @staticmethod
    def by_user(user_id):
        return list(Subscription.select().where(Subscription.user == user_id))

    @staticmethod
    def by_category(category_id):
        return list(Subscription.select().where(
            Subscription.category == category_id))
