"""
    UFind-API.__init__.py
    
    :copyright: (c) Feb 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.
"""
from peewee import Model

from app import db


class BaseModel(Model):

    def to_dict(self):
        """
            Make a dictionary of itself.
        :return: dict
        """
        raise NotImplementedError

    class Meta:
        database = db
