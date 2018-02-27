"""
    UFind-API.post
    
    :copyright: (c) Feb 2018 by Serey Morm.
    :license: BSD, see LICENSE for more details.
"""
import datetime

from peewee import *

from app import bcrypt
from . import BaseModel
from .user import User
 
class Post(BaseModel):
    """
        Representation of an post.
    """
    title = CharField()
    description = CharField()
    category = CharField()
    date = CharField()
    author = ForeignKeyField(User, related_name='author')
    created = DateTimeField(default=datetime.datetime.now())

    def __repr__(self):
        return "<title: {}, description: {}>".format(self.title, self.description)

    @staticmethod
    def get_post_by_id(post_id: int):
        return Post.get(Post.id == post_id)

    def update_with(self, title, description, category, date):
        self.title = title
        self.description = description
        self.category = category
        self.date = date

        self.save()

    def to_dict(self):
        """
            Make this object a dictionary.
        :return: dict
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date": self.date,
            "created": self.created
        }

    class NotFound(DoesNotExist):
        pass
