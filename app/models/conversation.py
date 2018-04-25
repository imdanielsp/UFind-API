"""
    UFind-API.conversation
    
    :copyright: (c) Apr 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.
"""
from peewee import *

from . import BaseModel
from app.models.user import User


class Conversation(BaseModel):
    """
    Represents a conversation
    """
    user_a = ForeignKeyField(User, backref="userA")
    user_b = ForeignKeyField(User, backref="userB")

    def __repr__(self):
        return "<Conversation: {} -> {}>".format(self.user_a, self.user_b)

    def to_dict(self):
        return {
            "id": self.id,
            "user_a": self.user_a.to_safe_dict(),
            "user_b": self.user_b.to_safe_dict()
        }

    @staticmethod
    def make_between(user_a, user_b):
        try:
            return Conversation.create(
                user_a=user_a,
                user_b=user_b
            )
        except IntegrityError:
            raise User.NotFound

    @staticmethod
    def by_user(user_a, user_b):
        """
        Gets the conversation between the users.
        :param user_a:
        :param user_b:
        :return:
        """
        if Conversation.exist_between(user_a, user_b):
            # Compound expression is working... doing it separate. FML
            conv = Conversation.raw("""
                SELECT * FROM `conversation` 
                WHERE (`user_a_id` = %s 
                  AND `user_b_id` = %s)
                  OR
                  (`user_a_id` = %s
                  AND `user_b_id` = %s)
            """, user_a, user_b, user_b, user_a)
            return conv.get()
        else:
            raise Conversation.NotFound

    @staticmethod
    def exist_between(user_a, user_b):
        try:
            c = Conversation.raw("""
                            SELECT * FROM `conversation` 
                            WHERE (`user_a_id` = %s 
                              AND `user_b_id` = %s)
                              OR
                              (`user_a_id` = %s
                              AND `user_b_id` = %s)
                        """, user_a, user_b, user_b, user_a).get()
        except DoesNotExist:
            return False
        return True

    @staticmethod
    def get_thread_of(user_id):
        def transformer(conv):
            conv_map = conv.to_dict()

            if conv_map["user_a"]["id"] != user_id:
                receiver = conv_map["user_a"]
            else:
                receiver = conv_map["user_b"]

            return {
                "conversation_id": conv_map["id"],
                "receiver": receiver,
                "last": None
            }

        def add_message(conv):
            from app.models.message import Message

            msgs = Message.select().where(
                Message.conversation == conv["conversation_id"]
            ).order_by(Message.sent_at.desc())
            msg = msgs.first()
            if msg:
                msg = msg.to_dict()
                msg.pop("sender")
                conv["last"] = msg
            return conv

        convs = list(Conversation.select().where(
            Conversation.user_a == user_id)) + list(
            Conversation.select().where(Conversation.user_b == user_id))

        return list(map(add_message, map(transformer, convs)))

    class NotFound(Exception):
        pass
