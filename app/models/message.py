"""
    UFind-API.message
    
    :copyright: (c) Apr 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.
"""
import datetime

from peewee import *

from . import BaseModel
from app.models.conversation import Conversation
from app.models.user import User


class Message(BaseModel):
    conversation = ForeignKeyField(Conversation, backref="conversations")
    sender = ForeignKeyField(User, backref="msg_sender")
    content = CharField()
    sent_at = DateTimeField(default=datetime.datetime.now)

    def __repr__(self):
        return "<Message: {} to {}>".format(self.sender, self.conversation)

    def to_dict(self):
        return {
            "conversation": self.conversation.id,
            "sender": self.sender.to_dict_without_picture(),
            "content": self.content,
            "sent_at": self.sent_at
        }

    @staticmethod
    def by_conversation(conversation):
        messages = Message.select().where(
            Message.conversation == conversation.id
        ).order_by(Message.sent_at.desc())

        return list(map(lambda msg: msg.to_dict(), messages))

    @staticmethod
    def add(conversation_id, sender_id, msg):
        return Message.create(
            conversation=conversation_id,
            sender=sender_id,
            content=msg
        )
