"""
    UFind-API.category
    
    :copyright: (c) Apr 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.
"""
from peewee import *

from . import BaseModel


class Category(BaseModel):
    """
    Represent the category collection of the API.
    """
    name = CharField()
    member_count = IntegerField(default=0)

    def __repr__(self):
        return "<Category: {} Count: {}>".format(self.name, self.member_count)

    @staticmethod
    def by_id(category_id: int):
        return Category.get(Category.id == category_id)

    def update_with(self, name):
        self.name = name
        self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "member_count": self.member_count
        }

    class DuplicateCategory(IntegrityError):
        pass

    @staticmethod
    def all():
        return list(map(lambda cat: cat.to_dict(), Category.select()))
